#!/usr/bin/env python3
"""Export an explanatory-animations widget HTML to a video file.

Usage:
    python3 export-widget.py --widget path/to/widget.html \\
                             --resolution 1080x1920 \\
                             --fps 60 \\
                             --duration 6 \\
                             --out reel.mp4

Requirements:
    pip install playwright
    python3 -m playwright install chromium
    ffmpeg installed and on PATH

The widget MUST expose its master timeline as `window.timeline` so the
script can seek frame-by-frame deterministically. See the "Export hook"
section of library/export.md and library/content-creator-uses.md.

The widget should also support `?clean=1` URL param to hide controls
during recording (already implemented in all bundled examples).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright not installed. Run:  pip install playwright && python3 -m playwright install chromium", file=sys.stderr)
    sys.exit(1)


def export_widget(
    widget: pathlib.Path,
    width: int,
    height: int,
    fps: int,
    duration_sec: float,
    out: pathlib.Path,
    *,
    device_scale_factor: int = 2,
    background_audio: pathlib.Path | None = None,
    narration_audio: pathlib.Path | None = None,
    crf: int = 18,
    preset: str = "slow",
    show_progress: bool = True,
) -> None:
    """Render `widget` to `out` MP4 by stepping its timeline frame-by-frame."""
    if not widget.exists():
        raise FileNotFoundError(widget)
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("ffmpeg not found on PATH. Install via brew/apt/choco.")

    total_frames = int(round(fps * duration_sec))
    frame_dir = pathlib.Path(tempfile.mkdtemp(prefix="anim-frames-"))

    print(f"🎬  Rendering {widget.name}")
    print(f"    target:   {width}×{height} @ {fps}fps   {duration_sec}s   {total_frames} frames")
    print(f"    frames →  {frame_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--font-render-hinting=none"])
        page = browser.new_page(
            viewport={"width": width // device_scale_factor, "height": height // device_scale_factor},
            device_scale_factor=device_scale_factor,
        )
        url = f"file://{widget.resolve()}?clean=1&export=1"
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.wait_for_function("typeof document.fonts !== 'undefined' && document.fonts.status === 'loaded'", timeout=8000)
        # Pause whatever timeline the widget exposes.
        page.evaluate(
            """() => {
              if (window.timeline) { window.timeline.pause(); window.timeline.seek(0); }
              if (window.anime && window.anime.engine) { window.anime.engine.speed = 1; }
            }"""
        )
        # Wait one frame so the first seek lands before capture.
        page.wait_for_timeout(60)

        # Frame-by-frame seek + screenshot.
        last_pct = -1
        for i in range(total_frames + 1):
            t_ms = (i / fps) * 1000
            page.evaluate(f"() => {{ if (window.timeline) window.timeline.seek({t_ms}); }}")
            page.wait_for_timeout(8)  # let the seek paint
            page.screenshot(path=str(frame_dir / f"frame-{i:06d}.png"), full_page=False)
            if show_progress:
                pct = (i * 100) // (total_frames + 1)
                if pct != last_pct and pct % 5 == 0:
                    print(f"    capture: {pct:3d}%   frame {i}/{total_frames}", end="\r", flush=True)
                    last_pct = pct
        browser.close()
    if show_progress:
        print()

    # Build ffmpeg command.
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frame_dir / "frame-%06d.png"),
    ]
    # Optional audio inputs
    audio_inputs: list[pathlib.Path] = []
    if narration_audio:
        cmd += ["-i", str(narration_audio)]
        audio_inputs.append(narration_audio)
    if background_audio:
        cmd += ["-i", str(background_audio)]
        audio_inputs.append(background_audio)

    cmd += [
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", preset,
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={width}:{height}:flags=lanczos",
    ]

    if len(audio_inputs) == 1:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    elif len(audio_inputs) == 2:
        # Mix narration (full) + background (15%)
        cmd += [
            "-filter_complex",
            "[2:a]volume=0.15[bg];[1:a][bg]amix=inputs=2:duration=first[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
        ]

    cmd += [str(out)]

    print(f"🛠   ffmpeg → {out}")
    subprocess.run(cmd, check=True)

    # Cleanup frames
    shutil.rmtree(frame_dir, ignore_errors=True)

    file_kb = out.stat().st_size // 1024
    print(f"✅  Done — {out}  ({file_kb} KB)")


def main():
    ap = argparse.ArgumentParser(description="Export an explanatory-animations widget HTML to MP4.")
    ap.add_argument("--widget", required=True, type=pathlib.Path, help="Path to the widget HTML file")
    ap.add_argument("--resolution", default="1920x1080", help="Output resolution WxH (e.g. 1080x1920 for shorts/reels, 1920x1080 for landscape)")
    ap.add_argument("--fps", type=int, default=60, help="Framerate (30 or 60). Default 60.")
    ap.add_argument("--duration", type=float, default=6.0, help="Total seconds to capture. Default 6.")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("video.mp4"), help="Output MP4 path. Default ./video.mp4")
    ap.add_argument("--device-scale", type=int, default=2, help="DPR for crisp text. Default 2.")
    ap.add_argument("--narration", type=pathlib.Path, help="Optional narration audio (mp3/wav/m4a)")
    ap.add_argument("--music",     type=pathlib.Path, help="Optional background music (mp3/wav/m4a) — mixed at 15%% volume under narration")
    ap.add_argument("--crf", type=int, default=18, help="x264 CRF (lower=better quality, larger file). Default 18.")
    ap.add_argument("--preset", default="slow", help="x264 preset. Default slow.")
    args = ap.parse_args()

    try:
        w, h = (int(x) for x in args.resolution.lower().split("x"))
    except ValueError:
        print(f"Invalid --resolution {args.resolution!r}. Use WxH like 1920x1080.", file=sys.stderr)
        sys.exit(2)

    try:
        export_widget(
            widget=args.widget,
            width=w, height=h,
            fps=args.fps,
            duration_sec=args.duration,
            out=args.out,
            device_scale_factor=args.device_scale,
            background_audio=args.music,
            narration_audio=args.narration,
            crf=args.crf,
            preset=args.preset,
        )
    except (FileNotFoundError, EnvironmentError) as e:
        print(f"❌  {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌  ffmpeg failed with code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
