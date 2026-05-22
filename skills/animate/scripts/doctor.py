#!/usr/bin/env python3
"""Preflight check for the explanatory-animations skill.

Reports what's installed, what's missing, and what bootstrapping would
download — WITHOUT installing anything. Use this:

  - From the agent: invoke before suggesting bootstrap, so the user
    sees a transparent breakdown ("will install X, will reuse Y").
  - From the user: `python3 doctor.py` to validate setup state.

Output: a JSON object on stdout, one human-readable summary block on
stderr. Exit code:
  0  READY    — everything needed is available, render.py will work
  1  NEEDS    — bootstrap required, no blockers (1st run case)
  2  BLOCKED  — missing prerequisites the script can't fix (Python<3.8,
                no internet to PyPI, no disk space, no write access)
"""
from __future__ import annotations

import json
import os
import pathlib
import platform
import shutil
import socket
import subprocess
import sys

CACHE_ROOT = pathlib.Path.home() / ".cache" / "explanatory-animations"
VENV_DIR   = CACHE_ROOT / "venv"
VENV_PY    = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "python"
STAMP_FILE = CACHE_ROOT / "deps-installed.stamp"

# Approx download sizes (informational, used for the "first time" warning).
SIZE_PLAYWRIGHT_PIP_MB = 50
SIZE_CHROMIUM_MB       = 150
SIZE_IMAGEIO_FFMPEG_MB = 25
SIZE_TOTAL_MB          = SIZE_PLAYWRIGHT_PIP_MB + SIZE_CHROMIUM_MB + SIZE_IMAGEIO_FFMPEG_MB

# Reasonable minimum disk space to require (target dir).
MIN_FREE_MB = 600


def _check_python() -> dict:
    ver = sys.version_info
    ok = (ver.major, ver.minor) >= (3, 8)
    return {
        "name": "python",
        "ok": ok,
        "version": f"{ver.major}.{ver.minor}.{ver.micro}",
        "needs_action": None if ok else "Upgrade to Python ≥ 3.8 (current: " + sys.version.split()[0] + ")",
    }


def _check_pip() -> dict:
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                       capture_output=True, check=True, timeout=10)
        return {"name": "pip", "ok": True, "version": "ok", "needs_action": None}
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return {"name": "pip", "ok": False, "version": None,
                "needs_action": "Install pip (usually shipped with Python; on Debian/Ubuntu run `apt install python3-pip`)"}


def _check_venv() -> dict:
    """Check whether venv module is importable AND the cache dir is writable."""
    try:
        subprocess.run([sys.executable, "-m", "venv", "--help"],
                       capture_output=True, check=True, timeout=5)
        venv_module_ok = True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        venv_module_ok = False

    # Writability: parent dir of CACHE_ROOT must be writable.
    parent = CACHE_ROOT.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        writable = os.access(parent, os.W_OK)
    except OSError:
        writable = False

    ok = venv_module_ok and writable
    return {
        "name": "venv",
        "ok": ok,
        "venv_module": venv_module_ok,
        "cache_writable": writable,
        "cache_dir": str(CACHE_ROOT),
        "needs_action":
            None if ok
            else "Install python venv (`apt install python3-venv`)" if not venv_module_ok
            else f"Make {parent} writable",
    }


def _check_system_ffmpeg() -> dict:
    """Reuse system ffmpeg if present (skip downloading imageio-ffmpeg)."""
    path = shutil.which("ffmpeg")
    if path:
        try:
            out = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=5)
            ver = (out.stdout.splitlines() or [""])[0]
            return {"name": "ffmpeg-system", "ok": True, "path": path, "version": ver, "will_skip_pip": True}
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
    return {"name": "ffmpeg-system", "ok": False, "path": None, "version": None, "will_skip_pip": False}


def _check_existing_venv() -> dict:
    """Detect whether the skill's private venv is already set up."""
    has_python = VENV_PY.exists()
    stamp_match = STAMP_FILE.exists()
    return {
        "name": "skill-venv",
        "ok": has_python and stamp_match,
        "venv_python": str(VENV_PY) if has_python else None,
        "stamp_present": stamp_match,
    }


def _check_disk_space() -> dict:
    """Verify CACHE_ROOT's parent has enough free space for the install."""
    parent = CACHE_ROOT.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
        usage = shutil.disk_usage(parent)
        free_mb = usage.free // (1024 * 1024)
        ok = free_mb >= MIN_FREE_MB
        return {"name": "disk-space", "ok": ok, "free_mb": free_mb, "required_mb": MIN_FREE_MB,
                "needs_action": None if ok else f"Free up disk space ({free_mb} MB free, need ≥{MIN_FREE_MB} MB)"}
    except OSError as e:
        return {"name": "disk-space", "ok": False, "free_mb": None, "required_mb": MIN_FREE_MB,
                "needs_action": f"Could not check disk space: {e}"}


def _check_network() -> dict:
    """Quick reachability check to PyPI + Playwright download server."""
    hosts = [("pypi.org", 443), ("playwright.azureedge.net", 443)]
    results = {}
    for host, port in hosts:
        try:
            with socket.create_connection((host, port), timeout=3):
                results[host] = True
        except (socket.timeout, OSError):
            results[host] = False
    ok = all(results.values())
    return {"name": "network", "ok": ok, "hosts": results,
            "needs_action": None if ok else f"Network not reachable: {[h for h, v in results.items() if not v]}"}


def _check_system_chromium() -> dict:
    """Best-effort check for an existing Chromium-family browser the user
    could repoint Playwright to via the PLAYWRIGHT_BROWSERS_PATH or by
    setting `executablePath` at launch time. Informational only."""
    candidates = ["chromium", "chrome", "google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for c in candidates:
        path = shutil.which(c) if not c.startswith("/") else (c if pathlib.Path(c).exists() else None)
        if path:
            return {"name": "chromium-system", "ok": True, "path": path}
    return {"name": "chromium-system", "ok": False, "path": None}


def run() -> int:
    checks = {
        "python":   _check_python(),
        "pip":      _check_pip(),
        "venv":     _check_venv(),
        "disk":     _check_disk_space(),
        "network":  _check_network(),
        "system_ffmpeg":   _check_system_ffmpeg(),
        "system_chromium": _check_system_chromium(),
        "skill_venv":      _check_existing_venv(),
    }

    blocked = any(not checks[k]["ok"] for k in ("python", "pip", "venv", "disk", "network"))
    ready = checks["skill_venv"]["ok"]

    if blocked:
        status = "BLOCKED"
        exit_code = 2
    elif ready:
        status = "READY"
        exit_code = 0
    else:
        status = "NEEDS_BOOTSTRAP"
        exit_code = 1

    # Plan: what will the bootstrap do?
    plan = []
    download_mb = 0
    if not checks["skill_venv"]["ok"]:
        plan.append(f"Create venv at {VENV_DIR}")
        plan.append(f"pip install playwright (~{SIZE_PLAYWRIGHT_PIP_MB} MB)")
        download_mb += SIZE_PLAYWRIGHT_PIP_MB
        if not checks["system_ffmpeg"]["ok"]:
            plan.append(f"pip install imageio-ffmpeg (~{SIZE_IMAGEIO_FFMPEG_MB} MB bundled binary)")
            download_mb += SIZE_IMAGEIO_FFMPEG_MB
        else:
            plan.append(f"Reuse system ffmpeg at {checks['system_ffmpeg']['path']} (skip imageio-ffmpeg download)")
        plan.append(f"playwright install chromium (~{SIZE_CHROMIUM_MB} MB)")
        download_mb += SIZE_CHROMIUM_MB

    report = {
        "status": status,
        "exit_code": exit_code,
        "platform": platform.platform(),
        "checks": checks,
        "bootstrap_plan": plan,
        "download_mb": download_mb,
        "cache_root": str(CACHE_ROOT),
        "min_free_mb_required": MIN_FREE_MB,
    }

    # JSON to stdout (for the agent).
    print(json.dumps(report, indent=2))

    # Human summary to stderr (for the user / dev).
    sys.stderr.write("\n")
    sys.stderr.write(f"[doctor] status: {status}\n")
    if status == "BLOCKED":
        sys.stderr.write("[doctor] blockers:\n")
        for k, c in checks.items():
            if not c.get("ok") and k in ("python", "pip", "venv", "disk", "network"):
                sys.stderr.write(f"  - {c['name']}: {c.get('needs_action') or 'not ok'}\n")
    elif status == "NEEDS_BOOTSTRAP":
        sys.stderr.write(f"[doctor] first-time setup will download ~{download_mb} MB into {CACHE_ROOT}\n")
        for step in plan:
            sys.stderr.write(f"  • {step}\n")
        if checks["system_chromium"]["ok"]:
            sys.stderr.write(f"[doctor] note: system Chromium detected at {checks['system_chromium']['path']} — playwright still downloads its own copy (different version, separate cache)\n")
    else:
        sys.stderr.write(f"[doctor] cache present at {VENV_DIR}\n")
    sys.stderr.write("\n")

    return exit_code


if __name__ == "__main__":
    sys.exit(run())
