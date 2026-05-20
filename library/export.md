# Export to video

Four strategies, pick based on automation needs and what's installed. The first (the bundled script) is the path the skill recommends by default — the others stay documented so power users have options.

## Ask the user first

When the user requests video export, confirm:

1. **Resolution**: `720p (1280×720)` / `1080p (1920×1080)` / `4K (3840×2160)` / `custom`
2. **Frame rate**: `30 fps` / `60 fps`
3. **Aspect ratio**: `16:9` / `9:16 (vertical, TikTok/Shorts)` / `1:1 (square, Instagram)` / `custom`
4. **Duration cap**: total seconds. If shorter than the animation at 1×, time-compress.
5. **Format**: `mp4 (H.264)` / `webm (VP9)` / `gif` (only if ≤6 s, animations longer than that should be video)
6. **With audio?** If yes, ask for narration script or background music track.

## Strategy 0 — The bundled `scripts/export-widget.py` (recommended)

The skill ships a one-shot Python script that drives the widget headlessly via **Playwright + Chromium**, screenshots every frame, and assembles the MP4 with **ffmpeg**. Supports optional narration + background music mixing.

```bash
# Install once
pip install playwright
python3 -m playwright install chromium
# (ffmpeg is also required — `brew install ffmpeg` / `apt install ffmpeg`)

# Export
python3 ${CLAUDE_SKILL_DIR}/scripts/export-widget.py \
    --widget my-widget.html \
    --resolution 1080x1920 \
    --fps 60 \
    --duration 6 \
    --out reel.mp4

# With narration + music
python3 ${CLAUDE_SKILL_DIR}/scripts/export-widget.py \
    --widget my-widget.html \
    --resolution 1920x1080 \
    --fps 60 \
    --duration 10 \
    --narration voiceover.mp3 \
    --music    background.mp3 \
    --out      final.mp4
```

**Conventions the widget MUST follow** for the script to work:

1. Expose its master timeline as `window.timeline` so the script can call `window.timeline.seek(t_ms)` frame-by-frame.
2. Honor `?clean=1` URL param to hide the controls strip during recording.
3. Wait for `document.fonts.ready` before any layout-sensitive work.

All bundled examples follow these conventions. When you generate a new widget from a pattern doc, follow the same — it's a 3-line addition:

```js
const tl = createTimeline({ /* ... */ });
window.timeline = tl;                                                // ← convention
const clean = new URLSearchParams(location.search).get("clean") === "1";
if (clean) document.querySelectorAll(".controls").forEach(el => el.style.display = "none");
```

Output reference:
- 1080p 60fps 10s ≈ 8-15 MB
- 4K 60fps 10s ≈ 25-40 MB
- 9:16 1080×1920 60fps 6s ≈ 6-10 MB

CLI flags (run `--help` for the full list):

| Flag | Default | Notes |
|---|---|---|
| `--widget` | required | Path to the HTML file |
| `--resolution` | `1920x1080` | `1080x1920` for shorts, `1080x1080` for square |
| `--fps` | `60` | `30` for smaller files, `60` for smoothness |
| `--duration` | `6` | Seconds to capture |
| `--out` | `video.mp4` | Output path |
| `--device-scale` | `2` | DPR for crisp text |
| `--narration` | — | Optional audio overlay (full volume) |
| `--music` | — | Optional background (mixed at 15% under narration) |
| `--crf` | `18` | x264 quality (lower = better, larger) |
| `--preset` | `slow` | x264 preset |

## Strategy 1 — Manual screen recording (fastest, no setup)

Best for: one-off exports, demos, when you don't need pixel-perfect output.

1. Set up your screen: light theme, hidden tabs, browser at exact target resolution.
2. macOS: `Cmd+Shift+5` → "Record selected portion" → drag the widget → record → trim.
3. Linux: `OBS Studio` → window capture → record.
4. Windows: `Game Bar` (`Win+G`) → record → save.
5. Re-encode to target codec/bitrate via `ffmpeg`:
   ```bash
   ffmpeg -i input.mov -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output.mp4
   ```

Pros: 0 setup. Cons: includes browser chrome, not pixel-perfect, requires display.

## Strategy 2 — CCapture.js (in-browser, no headless)

Best for: clean frames without browser chrome, no headless setup, runs from the user's browser.

Add CCapture to the widget:

```html
<script src="https://cdn.jsdelivr.net/npm/ccapture.js@1.1.0/build/CCapture.all.min.js"></script>
```

Override anime.js timing to use a manual clock:

```js
const FPS = 60;
const TOTAL_SEC = 10;
const TOTAL_FRAMES = FPS * TOTAL_SEC;

const capturer = new CCapture({
  format: 'webm',         // 'webm' | 'gif' | 'png' (frame sequence)
  framerate: FPS,
  verbose: true,
  display: true,          // show the recording progress overlay
});

function startExport() {
  capturer.start();
  let frame = 0;

  // Drive the timeline manually
  const tl = anime.timeline({ autoplay: false, ... });
  buildTimeline(tl);

  function step() {
    if (frame > TOTAL_FRAMES) {
      capturer.stop();
      capturer.save();  // triggers download
      return;
    }
    const t = (frame / TOTAL_FRAMES) * tl.duration;
    tl.seek(t);
    capturer.capture(document.querySelector(".widget"));
    frame++;
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
```

Pros: clean output, no browser chrome, runs in any browser. Cons: WebM only (re-encode for MP4), slower than realtime.

Convert to MP4 after:
```bash
ffmpeg -i output.webm -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output.mp4
```

## Strategy 3 — Puppeteer headless (automated, scriptable)

Best for: batch export, CI/CD, embedding in a deploy pipeline.

```js
// export.js
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
  await page.goto(`file://${path.resolve('widget.html')}`);

  // Inject CCapture or do frame-by-frame screenshots manually
  const TOTAL_FRAMES = 600; // 10s @ 60fps
  const framesDir = './frames';
  if (!fs.existsSync(framesDir)) fs.mkdirSync(framesDir);

  for (let i = 0; i < TOTAL_FRAMES; i++) {
    const t = i / 60; // seconds
    await page.evaluate((t) => {
      window.timeline.seek(t * 1000);
    }, t);
    await page.screenshot({
      path: `${framesDir}/frame-${String(i).padStart(5, '0')}.png`,
      omitBackground: false,
    });
  }
  await browser.close();
})();
```

Then assemble with ffmpeg:
```bash
ffmpeg -framerate 60 -i frames/frame-%05d.png \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  -vf "scale=1920:1080" output.mp4
```

Pros: pixel-perfect, automated, CI-friendly. Cons: requires Node.js + Puppeteer + ffmpeg setup.

## Aspect ratio strategy

| Target | Stage size | Notes |
|---|---|---|
| 16:9 (YouTube) | 1920×1080 | Default for landscape system diagrams |
| 9:16 (TikTok/Shorts) | 1080×1920 | Rotate the layout to vertical; cards stack |
| 1:1 (Instagram) | 1080×1080 | Crop the wide layout; may require redesign |

Don't force a 16:9 system flow into 9:16 by squashing — redesign the layout. Most patterns offer a "vertical" variant (see the pattern doc).

## Adding narration

If the user wants narration:
1. Capture the silent video first (any strategy above).
2. Generate or record audio separately (suggested: ElevenLabs / Resemble / human VO).
3. Combine:
   ```bash
   ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -c:a aac -b:a 192k -shortest final.mp4
   ```

## Adding background music

```bash
ffmpeg -i video.mp4 -i music.mp3 -filter_complex \
  "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=shortest[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac final.mp4
```

(Adjust `volume=0.15` to taste — music should sit well under narration.)

## Roadmap — Remotion integration

[Remotion](https://www.remotion.dev) is a React-based programmatic video framework: write components → render with `npx remotion render` → get an MP4. It's an excellent alternative for use cases the current pipeline doesn't cover cleanly:

- **In-browser export button** — a Remotion preview app served by the skill where the user previews the animation, clicks "Export", and downloads the MP4 without needing local ffmpeg or Playwright installed.
- **Server-side rendering at scale** — Remotion Lambda renders 100s of variants in parallel (e.g. personalized reels per customer).
- **Component reuse with the widgets** — port a pattern's anime.js + SVG output into a `<Composition>` so the same animation works both as a standalone HTML widget (for embedding in docs) and as a Remotion clip (for batch video rendering).

Why not now: Remotion requires a React+Node toolchain, which adds friction for the "I just want one MP4" case Strategy 0 already covers. The plan when it lands:

```
scripts/
├── export-widget.py        # current — Playwright + ffmpeg (any HTML widget)
└── export-remotion/        # planned — React + Remotion (composable, batchable, server-renderable)
    ├── compositions/
    │   ├── lifecycle.tsx
    │   ├── system-flow.tsx
    │   ├── text-effect.tsx
    │   └── ...
    └── render.config.ts
```

Plus a documented bridge: any anime.js timeline can be wrapped in a Remotion `<Composition>` by mapping `frame → seek(frame * 1000 / fps)`, so the same source-of-truth animation drives both the standalone HTML widget AND the Remotion render.

**Want this now?** Tell the skill "use Remotion" and it can scaffold a React project that imports the widget's animation logic as a Remotion composition.

## Mistakes to avoid

1. **Recording during animation auto-play** — start the timeline manually at frame 0, don't rely on auto-play timing.
2. **Wrong aspect ratio** — confirm target ratio with user before recording; redesigning a 16:9 system flow as 9:16 is significant work.
3. **VBR (variable bitrate) codecs** for short clips — leads to inconsistent frame timing. Use CFR / `-vsync cfr`.
4. **No `pix_fmt yuv420p`** — videos won't play on iOS / older browsers / some social platforms.
5. **CCapture.js without `requestAnimationFrame`** — drops frames. Always drive `step()` via rAF.
