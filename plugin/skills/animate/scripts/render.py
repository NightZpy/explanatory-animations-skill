#!/usr/bin/env python3
"""Autonomous renderer for the explanatory-animations skill.

The agent invokes THIS script — never touches Playwright / ffmpeg / Node
directly. On first run it bootstraps a private venv under
~/.cache/explanatory-animations/venv, installs Playwright + imageio-ffmpeg
+ Chromium, then re-launches itself inside that venv. Subsequent runs
skip bootstrap (under 200ms cold).

The agent picks one of two modes:

  MODE: preview (default)
      Serves the widget on localhost and prints the URL.
      The agent hands that URL to the user — they open it in any browser.
      Server runs until Ctrl+C OR until --timeout seconds pass.

  MODE: video
      Renders the widget headlessly via Playwright + bundled ffmpeg, writes
      an MP4 to --out. The agent hands the file path to the user.

In both modes the widget must follow the conventions documented in
library/controls.md and library/export.md:
  - expose its master timeline as window.timeline
  - honor ?clean=1 to hide its controls strip during recording

Usage from the agent's perspective:

    # The agent wrote a widget at /tmp/anim/widget.html
    python3 scripts/render.py --widget /tmp/anim/widget.html
    # → prints "http://localhost:8765/widget.html  (Ctrl+C to stop)"

    python3 scripts/render.py --widget /tmp/anim/widget.html \\
        --out /tmp/anim/reel.mp4 \\
        --resolution 1080x1920 --fps 60 --duration 6
    # → prints "/tmp/anim/reel.mp4 (8.3 MB, 6s, 1080x1920)"
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import webbrowser

# ───────────────────────────────────────────────────────────────────────
#  Self-bootstrap stage (runs in the host Python, before any third-party imports)
# ───────────────────────────────────────────────────────────────────────

CACHE_ROOT = pathlib.Path.home() / ".cache" / "explanatory-animations"
VENV_DIR   = CACHE_ROOT / "venv"
VENV_PY    = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "python"
VENV_PIP   = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "pip"
STAMP_FILE = CACHE_ROOT / "deps-installed.stamp"
DEPS_VERSION = "v2"   # bump invalidates cache (last change: system-ffmpeg reuse)

REQUIRED_PIP_BASE   = ["playwright>=1.46"]
REQUIRED_PIP_FFMPEG = ["imageio-ffmpeg>=0.5"]


def _log(msg: str) -> None:
    sys.stdout.write(f"[render] {msg}\n")
    sys.stdout.flush()


def _in_venv() -> bool:
    return pathlib.Path(sys.executable).resolve() == VENV_PY.resolve()


def _have_system_ffmpeg() -> str | None:
    """Return the path to system ffmpeg if it's installed, else None."""
    p = shutil.which("ffmpeg")
    if not p:
        return None
    try:
        subprocess.run([p, "-version"], capture_output=True, check=True, timeout=5)
        return p
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None


def _prompt_consent(default_yes: bool, will_install_ffmpeg: bool) -> bool:
    """Ask the user before downloading ~200 MB. If --yes was passed OR
    stdin isn't a TTY (agent invocation), accept the default."""
    mb = 200 if will_install_ffmpeg else 175
    msg = (
        f"\n[render] First-time setup for the explanatory-animations skill:\n"
        f"  • Create private venv at {VENV_DIR}\n"
        f"  • Download Playwright + Chromium + ffmpeg helpers (~{mb} MB)\n"
        f"  • No system-wide changes — everything lives under ~/.cache/\n"
        f"  • Future runs reuse this cache and start in <200 ms\n"
    )
    if will_install_ffmpeg:
        msg += "  • System ffmpeg NOT found — will install bundled imageio-ffmpeg wheel\n"
    else:
        msg += "  • System ffmpeg detected — will reuse it (skip imageio-ffmpeg download)\n"
    sys.stderr.write(msg)
    if default_yes or not sys.stdin.isatty():
        sys.stderr.write("[render] proceeding (auto-yes — pass --no-bootstrap to abort)\n")
        return True
    sys.stderr.write("[render] continue? [Y/n] ")
    sys.stderr.flush()
    ans = sys.stdin.readline().strip().lower()
    return ans in ("", "y", "yes", "s", "si", "sí")


def _bootstrap_and_relaunch(consent: bool) -> None:
    """Build venv, install deps + chromium, then re-exec inside the venv.

    Idempotent: second call is a no-op aside from the stamp check.
    Honors a `--no-bootstrap` flag to abort cleanly if the user said no.
    """
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    system_ffmpeg = _have_system_ffmpeg()
    need_consent = not VENV_PY.exists() or not (STAMP_FILE.exists() and STAMP_FILE.read_text().strip() == DEPS_VERSION)

    if need_consent and not consent:
        agreed = _prompt_consent(default_yes=False, will_install_ffmpeg=(system_ffmpeg is None))
        if not agreed:
            sys.stderr.write("[render] aborted by user — re-run with --yes to skip the prompt next time\n")
            sys.exit(3)

    # Build venv if missing.
    if not VENV_PY.exists():
        _log(f"creating venv at {VENV_DIR}")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

    # (Re)install deps if stamp missing / version mismatch.
    stamp_ok = STAMP_FILE.exists() and STAMP_FILE.read_text().strip() == DEPS_VERSION
    if not stamp_ok:
        _log("upgrading pip")
        subprocess.check_call([str(VENV_PIP), "install", "--quiet", "--upgrade", "pip"])
        deps = list(REQUIRED_PIP_BASE)
        if system_ffmpeg is None:
            deps += REQUIRED_PIP_FFMPEG
            _log("installing playwright + imageio-ffmpeg")
        else:
            _log(f"installing playwright (reusing system ffmpeg at {system_ffmpeg})")
        subprocess.check_call([str(VENV_PIP), "install", "--quiet", *deps])
        # Chromium for Playwright.
        _log("downloading Chromium for Playwright (largest step, ~150 MB)")
        try:
            subprocess.check_call([str(VENV_PY), "-m", "playwright", "install", "chromium"])
        except subprocess.CalledProcessError:
            _log("warning: playwright chromium install returned non-zero — continuing anyway")
        STAMP_FILE.write_text(DEPS_VERSION)
        _log(f"done — cache will be reused next time ({VENV_DIR})")

    # Re-launch ourselves inside the venv.
    os.execv(str(VENV_PY), [str(VENV_PY), __file__, *sys.argv[1:]])


# Bootstrap if we're not already in the venv. After execv we resume in the venv.
if not _in_venv():
    # Side commands that don't need the venv at all.
    if "--doctor" in sys.argv:
        doctor_path = pathlib.Path(__file__).resolve().parent / "doctor.py"
        os.execv(sys.executable, [sys.executable, str(doctor_path)])

    consent = ("--yes" in sys.argv) or ("-y" in sys.argv)
    no_bootstrap = "--no-bootstrap" in sys.argv

    if no_bootstrap and not (VENV_PY.exists() and STAMP_FILE.exists()):
        sys.stderr.write(
            "[render] --no-bootstrap set but the skill venv is not ready. "
            "Run `python3 scripts/doctor.py` to see what's needed, then retry without --no-bootstrap.\n"
        )
        sys.exit(2)

    _bootstrap_and_relaunch(consent=consent)


# ───────────────────────────────────────────────────────────────────────
#  From here on we're guaranteed to be running inside the venv with
#  playwright (+ maybe imageio_ffmpeg) importable. ffmpeg may also be
#  on the system PATH — prefer system if present.
# ───────────────────────────────────────────────────────────────────────

from playwright.sync_api import sync_playwright   # type: ignore

def _resolve_ffmpeg() -> str:
    """Prefer system ffmpeg; fall back to imageio-ffmpeg wheel binary."""
    sys_path = shutil.which("ffmpeg")
    if sys_path:
        return sys_path
    try:
        import imageio_ffmpeg  # type: ignore
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise EnvironmentError(
            "ffmpeg is not available. Install it system-wide (`brew install ffmpeg` / "
            "`apt install ffmpeg` / `choco install ffmpeg`) OR rerun without "
            "--no-bootstrap so the script can install imageio-ffmpeg."
        )

FFMPEG = _resolve_ffmpeg()


# ───────────────────────────────────────────────────────────────────────
#  Mode: video
# ───────────────────────────────────────────────────────────────────────

def render_video(
    widget: pathlib.Path,
    width: int,
    height: int,
    fps: int,
    duration_sec: float,
    out: pathlib.Path,
    *,
    device_scale_factor: int = 2,
    narration_audio: pathlib.Path | None = None,
    background_audio: pathlib.Path | None = None,
    crf: int = 18,
) -> None:
    if not widget.exists():
        raise FileNotFoundError(widget)

    total_frames = int(round(fps * duration_sec))
    frame_dir = pathlib.Path(tempfile.mkdtemp(prefix="anim-frames-"))

    _log(f"rendering {widget.name} → {out}")
    _log(f"  {width}×{height} @ {fps}fps × {duration_sec}s = {total_frames} frames")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--font-render-hinting=none"])
        page = browser.new_page(
            viewport={"width": width // device_scale_factor, "height": height // device_scale_factor},
            device_scale_factor=device_scale_factor,
        )
        page.goto(f"file://{widget.resolve()}?clean=1&export=1")
        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_function(
                "typeof document.fonts !== 'undefined' && document.fonts.status === 'loaded'",
                timeout=8000,
            )
        except Exception:
            pass
        page.evaluate(
            """() => {
              if (window.timeline) { window.timeline.pause(); window.timeline.seek(0); }
              if (window.anime && window.anime.engine) { window.anime.engine.speed = 1; }
            }"""
        )
        page.wait_for_timeout(60)

        last_pct = -5
        for i in range(total_frames + 1):
            t_ms = (i / fps) * 1000
            page.evaluate(f"() => {{ if (window.timeline) window.timeline.seek({t_ms}); }}")
            page.wait_for_timeout(8)
            page.screenshot(path=str(frame_dir / f"frame-{i:06d}.png"), full_page=False)
            pct = (i * 100) // (total_frames + 1)
            if pct - last_pct >= 5:
                sys.stdout.write(f"\r[render]   capture: {pct:3d}%  ({i}/{total_frames})")
                sys.stdout.flush()
                last_pct = pct
        sys.stdout.write("\n")
        browser.close()

    # Assemble MP4 via bundled ffmpeg.
    cmd = [
        FFMPEG, "-y",
        "-framerate", str(fps),
        "-i", str(frame_dir / "frame-%06d.png"),
    ]
    audio_inputs: list[pathlib.Path] = []
    if narration_audio: cmd += ["-i", str(narration_audio)]; audio_inputs.append(narration_audio)
    if background_audio: cmd += ["-i", str(background_audio)]; audio_inputs.append(background_audio)

    cmd += [
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={width}:{height}:flags=lanczos",
    ]
    if len(audio_inputs) == 1:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    elif len(audio_inputs) == 2:
        cmd += [
            "-filter_complex",
            "[2:a]volume=0.15[bg];[1:a][bg]amix=inputs=2:duration=first[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
        ]
    cmd += [str(out)]

    _log("encoding MP4 (bundled ffmpeg)")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(frame_dir, ignore_errors=True)

    size_kb = out.stat().st_size // 1024
    print(json.dumps({
        "mode": "video",
        "out": str(out),
        "size_kb": size_kb,
        "resolution": f"{width}x{height}",
        "fps": fps,
        "duration_sec": duration_sec,
    }))
    _log(f"done → {out}  ({size_kb} KB)")


# ───────────────────────────────────────────────────────────────────────
#  Mode: preview
# ───────────────────────────────────────────────────────────────────────

def serve_preview(widget: pathlib.Path, *, port: int | None = None,
                  timeout_sec: int | None = None, open_browser: bool = True) -> None:
    """Serve the widget over HTTP, print the URL, optionally auto-open the browser."""
    if not widget.exists():
        raise FileNotFoundError(widget)

    serve_dir = widget.parent.resolve()
    rel_name = widget.name

    if port is None:
        # Find a free ephemeral port.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

    import http.server
    import socketserver
    import threading

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_): pass
        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

    os.chdir(serve_dir)
    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    httpd.allow_reuse_address = True
    url = f"http://localhost:{port}/{rel_name}"

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    # Machine-readable JSON line (the agent uses this).
    print(json.dumps({"mode": "preview", "url": url, "serve_dir": str(serve_dir), "port": port}))
    _log(f"preview → {url}")
    _log(f"  serve dir: {serve_dir}")
    _log("  Ctrl+C to stop")

    if open_browser:
        webbrowser.open_new_tab(url)

    try:
        start = time.time()
        while True:
            if timeout_sec and (time.time() - start) >= timeout_sec:
                _log(f"timeout after {timeout_sec}s — shutting down")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        _log("shutting down")
    finally:
        httpd.shutdown()


# ───────────────────────────────────────────────────────────────────────
#  CLI
# ───────────────────────────────────────────────────────────────────────

def parse_resolution(s: str) -> tuple[int, int]:
    try:
        w, h = (int(x) for x in s.lower().split("x"))
        return w, h
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"--resolution must be WxH (e.g. 1920x1080) — got {s!r}") from e


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--widget", required=True, type=pathlib.Path, help="Path to the widget HTML file")
    ap.add_argument("--out", type=pathlib.Path, default=None,
                    help="If set, render to this MP4 (mode: video). If omitted, serve a preview URL.")
    ap.add_argument("--resolution", type=parse_resolution, default=(1920, 1080),
                    help="MP4 only — output resolution WxH. Default 1920x1080.")
    ap.add_argument("--fps", type=int, default=60, help="MP4 only — framerate. Default 60.")
    ap.add_argument("--duration", type=float, default=6.0, help="MP4 only — seconds. Default 6.")
    ap.add_argument("--device-scale", type=int, default=2, help="MP4 only — DPR. Default 2.")
    ap.add_argument("--narration", type=pathlib.Path, help="MP4 only — narration audio overlay")
    ap.add_argument("--music",     type=pathlib.Path, help="MP4 only — background music (mixed at 15%%)")
    ap.add_argument("--crf", type=int, default=18, help="MP4 only — x264 quality. Default 18.")

    ap.add_argument("--yes", "-y", action="store_true", help="Auto-accept first-run install prompt (default in non-TTY).")
    ap.add_argument("--no-bootstrap", action="store_true", help="Refuse to install anything; require the cache to be ready.")
    ap.add_argument("--doctor", action="store_true", help="Run the doctor script (preflight check) instead of rendering.")

    ap.add_argument("--port", type=int, default=None, help="Preview only — bind a specific port.")
    ap.add_argument("--timeout", type=int, default=None,
                    help="Preview only — auto-shutdown after N seconds (useful for one-shot agent runs).")
    ap.add_argument("--no-open", action="store_true",
                    help="Preview only — don't open a browser tab automatically.")
    args = ap.parse_args()

    if args.out is not None:
        w, h = args.resolution
        try:
            render_video(
                widget=args.widget,
                width=w, height=h, fps=args.fps, duration_sec=args.duration,
                out=args.out,
                device_scale_factor=args.device_scale,
                narration_audio=args.narration,
                background_audio=args.music,
                crf=args.crf,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            _log(f"error: {e}")
            return 1
    else:
        try:
            serve_preview(
                args.widget,
                port=args.port,
                timeout_sec=args.timeout,
                open_browser=not args.no_open,
            )
        except (FileNotFoundError, OSError) as e:
            _log(f"error: {e}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
