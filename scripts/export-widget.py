#!/usr/bin/env python3
"""Backward-compatible alias — forwards to scripts/render.py.

The skill's autonomous renderer is now render.py, which handles BOTH
preview-URL and MP4 modes with auto-bootstrap of deps in ~/.cache.
This file remains so old invocations keep working.
"""
import os, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
os.execv(sys.executable, [sys.executable, str(here / "render.py"), *sys.argv[1:]])
