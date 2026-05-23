---
name: export-widget
description: Render an existing animation widget HTML to a preview URL or an MP4 file. Use when the user has a widget already (built by `build-widget` or hand-rolled) and wants to see it in a browser, share a URL, or get a video file. Auto-installs Playwright + Chromium + ffmpeg in `~/.cache/explanatory-animations/venv` on first use — the user does NOT install anything manually.
---

This skill drives the autonomous renderer at `../animate/scripts/render.py`. It handles BOTH preview-URL serving AND headless MP4 export. The user installs nothing — the script bootstraps a private venv with Playwright + Chromium + bundled ffmpeg (via `imageio-ffmpeg`) on first run. Subsequent runs reuse the cache (<200ms cold start).

## First-time setup contract (MARKETPLACE-IMPORTANT)

**Before** invoking `render.py` for the first time on a user's machine, the agent MUST:

1. Run `python3 ${CLAUDE_SKILL_DIR}/../animate/scripts/doctor.py` first.
2. Parse the JSON output — three possible statuses:
   - `READY` → cache already present, proceed silently.
   - `NEEDS_BOOTSTRAP` → first run. **Show the user the `bootstrap_plan` array + `download_mb`** so they know what's about to happen. Get explicit consent before invoking render.py.
   - `BLOCKED` → the script can't fix it (Python < 3.8, no network, etc.). Show the user the blocker from `checks[*].needs_action` and stop.
3. After consent, invoke `render.py --yes ...` so the script doesn't re-prompt.

Sample agent message (NEEDS_BOOTSTRAP case):

> Para exportar este widget necesito instalar Playwright + Chromium (≈175 MB)
> en `~/.cache/explanatory-animations/`. Esto es aislado — no toca tu sistema
> y se reusa siempre que vuelvas a exportar. Tu ffmpeg ya está instalado, así
> que lo reuso. ¿Procedo? (la próxima vez no te pregunto, es solo la primera.)

Sample agent message (READY case): silent — just proceed.

Sample agent message (BLOCKED case): show the blocker, stop.

`scripts/doctor.py` doubles as the user's "is this working?" check — they can run it manually anytime.

## Inputs

1. **Widget path** (required) — path to the `.html` file.
2. **Mode**:
   - `preview` (default if no `--out`) — serve on localhost, print URL, optionally auto-open browser.
   - `video` (when `--out X.mp4` is given) — headless render to MP4.
3. **For video mode**:
   - Resolution (`1920x1080` / `1080x1920` / `1080x1080` / custom)
   - FPS (`30` / `60`)
   - Duration (seconds)
   - Optional narration audio (`--narration foo.mp3`)
   - Optional background music (`--music bg.mp3` mixed at 15% under narration)

## How to invoke

```bash
# Preview URL — auto-opens browser, runs until Ctrl+C or --timeout
python3 ${CLAUDE_SKILL_DIR}/../animate/scripts/render.py \
    --widget /tmp/anim/widget.html

# Video file
python3 ${CLAUDE_SKILL_DIR}/../animate/scripts/render.py \
    --widget /tmp/anim/widget.html \
    --out /tmp/anim/reel.mp4 \
    --resolution 1080x1920 \
    --fps 60 \
    --duration 6

# With narration + music
python3 ${CLAUDE_SKILL_DIR}/../animate/scripts/render.py \
    --widget /tmp/anim/widget.html \
    --out /tmp/anim/final.mp4 \
    --resolution 1920x1080 --fps 60 --duration 10 \
    --narration voiceover.mp3 \
    --music bg.mp3
```

Both modes emit a single JSON line to stdout that the agent parses and hands to the user:

- preview: `{"mode":"preview","url":"http://localhost:54321/widget.html",...}`
- video:   `{"mode":"video","out":"/tmp/anim/reel.mp4","size_kb":8345,...}`

## Widget conventions the widget MUST follow

The script seeks the timeline manually frame-by-frame. Skill-generated widgets follow these by default (see `../animate/library/export.md`), but verify before rendering:

1. `window.timeline` is exposed — the master timeline must be reachable.
2. `?clean=1` URL param hides the controls strip — applied automatically by `render.py`.
3. `document.fonts.ready` is awaited before layout-sensitive work.

If the widget doesn't follow these, either:
- Fix the widget first (1 line: `window.timeline = tl;` after the `createTimeline` call), OR
- Tell the user to use Strategy 0 (in-widget Export button via `add-export-button`) which is more forgiving.

## When to hand off

- **The user wants a one-click Export inside the open widget** → use `add-export-button` instead (no Playwright bootstrap needed, just one script tag).
- **The user wants in-browser preview with live props panel + Render button** → suggest Remotion (Strategy 5 in `../animate/library/export.md`).
- **The user has no widget yet** → run `build-widget` first.

## Referenced files

- `../animate/scripts/render.py` — the engine. Reads `--help` for the full flag list.
- `../animate/library/export.md` — full pipeline docs (6 strategies, conventions, output sizes).
- `../animate/library/content-creator-uses.md` — guidance on aspect ratios / fps for social-media exports.

## Pitfalls

- **First run takes ~30-60 seconds** (Playwright + Chromium download). The agent should warn the user the first time only. After that, ~5-15 sec for a 6s clip.
- **Widget without `window.timeline`** → render produces a static first frame loop. Fix the widget.
- **`--out` with relative path** → resolved against the script's CWD, not the agent's. Always pass absolute paths.
- **Aspect ratio mismatch** with widget viewBox → letterboxed output. Pre-design the widget for the target ratio.
