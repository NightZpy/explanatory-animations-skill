---
name: add-export-button
description: Inject a floating "⬇ Export" button into an existing animation widget HTML so the user can record + download it from the browser themselves. No server, no Playwright, no Node. Use when the user already has a widget HTML (built by `build-widget` or hand-rolled) and wants the click-to-export UX. Adds ONE `<script>` tag and verifies the widget exposes `window.timeline`.
---

This skill adds **one `<script>` tag** to an existing widget HTML so a floating Export button appears in the bottom-right. The user clicks it → modal opens with aspect / resolution / fps / duration → click "Start recording" → browser steps through `window.timeline` frame-by-frame, rasterizes via `html2canvas`, and saves WebM to Downloads/.

No server. No Playwright. No bootstrap. Just edit the HTML file.

## Inputs

1. **Widget HTML path** (required).

## Process

1. Read the widget HTML.
2. Confirm the widget exposes `window.timeline` somewhere in its `<script>` block. If not, ask the user OR fix it: add `window.timeline = tl;` immediately after the timeline is created.
3. Inject this line just before `</body>`:

   ```html
   <script src="../widget-helpers/export-button.js" defer></script>
   ```

   Adjust the path so it points to `../animate/widget-helpers/export-button.js` relative to where the widget HTML lives, OR copy `export-button.js` next to the widget if portability matters.

4. Confirm to the user: "Done. Reload the widget in the browser — you'll see a floating '⬇ Export' button bottom-right."

## What the user gets

When they click the button:

- A modal opens with controls for **aspect** (16:9 / 9:16 / 1:1 / current), **resolution** (720p / 1080p / 1440p / 4K), **fps** (30 / 60), **duration** (1-60 seconds).
- Pre-fills duration from `window.timeline.duration` if it's a finite value.
- On "Start recording", lazy-loads CCapture.js (jsDelivr primary + unpkg fallback — not on cdnjs) and html2canvas (cdnjs primary + jsDelivr/unpkg fallback), ~150KB total. Steps the timeline, captures every frame, saves as `animation-WxH-timestamp.webm` to Downloads.
- A progress bar shows percent + frame count during recording.

## When to defer

- **User wants MP4 directly without the in-browser flow** → use `export-widget` (runs Playwright headless + bundled ffmpeg).
- **User has multiple widgets to batch-export** → use `export-widget` in a loop (in-widget recording is one-at-a-time by definition).
- **User wants the widget AND the Export button in the same emit** → `build-widget` already does this when the user said "I want to export from the browser" in discovery. This skill is for retrofitting existing widgets.

## Path resolution

Since plugin skills resolve `${CLAUDE_SKILL_DIR}` to their own directory, the `<script src="…/export-button.js">` reference must reach into the sibling skill `animate`. Two ways to handle this depending on where the widget HTML lives:

- **Inside this plugin's `examples/`**: `<script src="../widget-helpers/export-button.js" defer></script>` (already the convention).
- **Anywhere else**: copy `${CLAUDE_SKILL_DIR}/../animate/widget-helpers/export-button.js` next to the widget HTML and reference it as `<script src="export-button.js" defer></script>`. The script is fully self-contained (no other dependencies bundled with it).

## Referenced files

- `../animate/widget-helpers/export-button.js` — the actual module (drop-in, CCapture + html2canvas, no bundle, no setup).
- `../animate/library/export.md` § "Strategy 0 — In-widget Export button" — full behaviour reference + pitfalls.

## Pitfalls

- **Widget without `window.timeline`** → the button records but produces a static first frame. Fix the widget first.
- **`<script>` placed inside `<head>`** instead of before `</body>` → race conditions; the button can fire before the DOM is ready. Always before `</body>`.
- **CORS-tainted external images / fonts** → `html2canvas` skips them silently, so the WebM looks broken. Use CORS-friendly sources (Google Fonts is fine; arbitrary CDN images need their `Access-Control-Allow-Origin` header).
- **SVG filters (drop-shadow, blur)** sometimes render differently from the live widget. Inspect a test export before claiming "done".
