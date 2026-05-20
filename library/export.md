# Export to video

Five strategies, pick based on automation needs and what's installed. Strategy 0 (Python script) and Strategy 4 (Remotion) are bundled with the skill; the rest stay documented for the cases where bundling doesn't help.

**Quick chooser:**

| You want… | Strategy |
|---|---|
| **Autonomous: agent gives user a URL or MP4 with zero setup** | **0 — `scripts/render.py`** (auto-bootstraps deps in ~/.cache) |
| Live preview + Render button in a Studio with props panel | **4 — Remotion** (`scripts/export-remotion/`) |
| Server-side / Lambda render at scale, batch personalization | **4 — Remotion** (Lambda mode) |
| Quick one-off demo, recording from screen | **1 — Manual** |
| WebM frames-by-rAF without Node | **2 — CCapture.js** |
| Custom Node + Puppeteer pipeline in CI | **3 — Puppeteer** |

## Ask the user first

When the user requests video export, confirm:

1. **Resolution**: `720p (1280×720)` / `1080p (1920×1080)` / `4K (3840×2160)` / `custom`
2. **Frame rate**: `30 fps` / `60 fps`
3. **Aspect ratio**: `16:9` / `9:16 (vertical, TikTok/Shorts)` / `1:1 (square, Instagram)` / `custom`
4. **Duration cap**: total seconds. If shorter than the animation at 1×, time-compress.
5. **Format**: `mp4 (H.264)` / `webm (VP9)` / `gif` (only if ≤6 s, animations longer than that should be video)
6. **With audio?** If yes, ask for narration script or background music track.

## Strategy 0 — `scripts/render.py` (autonomous, the skill's default)

The agent (not the user) invokes `scripts/render.py`. On first run it auto-bootstraps a private venv at `~/.cache/explanatory-animations/venv` with Playwright + Chromium + a bundled ffmpeg (via `imageio-ffmpeg`). The user installs nothing. Second run is cached and starts in <200ms.

Two modes — `--out` flag chooses:

```bash
# Preview URL — agent serves the widget on localhost and prints the URL
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py --widget /tmp/anim/widget.html
#   → opens a browser tab + emits JSON: {"mode":"preview","url":"http://localhost:54321/widget.html"}
#   → server runs until Ctrl+C or --timeout seconds

# MP4 file — render headlessly and write the file
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py \
    --widget /tmp/anim/widget.html \
    --out    /tmp/anim/reel.mp4 \
    --resolution 1080x1920 \
    --fps 60 \
    --duration 6
#   → emits JSON: {"mode":"video","out":"...reel.mp4","size_kb":8345,...}

# With audio overlays
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py \
    --widget   /tmp/anim/widget.html \
    --out      /tmp/anim/final.mp4 \
    --resolution 1920x1080 --fps 60 --duration 10 \
    --narration voiceover.mp3 \
    --music     background.mp3
```

For preview mode, `--timeout 90` is useful in agent contexts so the server doesn't hang forever; `--no-open` skips the browser auto-open. For video mode, `--device-scale 2` (the default) keeps text crisp at any output resolution.

### Widget conventions the agent MUST embed

The script seeks the timeline manually frame-by-frame. The widget must expose:

```js
const tl = createTimeline({ /* ... */ });
window.timeline = tl;                                                // ← required
const clean = new URLSearchParams(location.search).get("clean") === "1";
if (clean) document.querySelectorAll(".controls, .sm-controls").forEach(el => el.style.display = "none");
```

All bundled examples and pattern-doc skeletons follow this — the agent must keep doing it when generating new widgets.

### Output reference

| Spec | Approx size |
|---|---|
| 1080p 60fps × 10s | 8–15 MB |
| 4K   60fps × 10s | 25–40 MB |
| 9:16 1080×1920 60fps × 6s | 6–10 MB |

### CLI flags

Run `python3 scripts/render.py --help` for the full list. Most common:

| Flag | Default | Notes |
|---|---|---|
| `--widget` | required | Path to the HTML |
| `--out` | — | Set to write MP4; omit for preview URL |
| `--resolution` | `1920x1080` | `1080x1920` shorts · `1080x1080` square |
| `--fps` | `60` | `30` for smaller files |
| `--duration` | `6` | Seconds (video mode only) |
| `--narration` | — | Audio overlay (full volume) |
| `--music` | — | Background music (mixed at 15%) |
| `--timeout` | — | Preview mode auto-shutdown after N seconds |
| `--no-open` | — | Preview mode — skip auto-opening browser |

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

## Strategy 4 — Remotion (in-browser preview + Export button)

[Remotion](https://www.remotion.dev) is a React-based programmatic video framework. The skill ships compositions under `scripts/export-remotion/` so the user gets:

- **Live preview + Export UI in the browser** (Remotion Studio). Pick composition → tweak props → click Render → download MP4. No manual ffmpeg config.
- **Headless CLI render** for CI / scripted exports.
- **Server-side / Lambda rendering at scale** (e.g. personalized reels per customer in batch).

```bash
cd scripts/export-remotion
npm install               # first time only (~250 MB, includes Chromium)
npm start                 # opens Remotion Studio at http://localhost:3000
```

Click **Render** in the Studio sidebar → MP4 lands in `out/`.

CLI for headless renders:
```bash
npx remotion render Lifecycle out/lifecycle.mp4

# with custom props
npx remotion render Lifecycle out/order.mp4 \
  --props='{"title":"Order lifecycle","path":["queued","paid","shipped","delivered"]}'

# vertical variant
npx remotion render LifecycleVertical out/lifecycle-9-16.mp4
```

Currently bundled compositions: `Lifecycle` / `LifecycleVertical` (Pattern A), `TextScramble` / `TextScrambleVertical` (Pattern M). Adding more is a 30-line file per pattern — see `scripts/export-remotion/README.md` for the template.

### Why Remotion vs the Python script

| Aspect | Strategy 0 (Python) | Strategy 4 (Remotion) |
|---|---|---|
| Setup | `pip install playwright` + `ffmpeg` | `npm install` (one-time, ~250 MB) |
| Source | Any HTML widget the skill produced | React components in `src/compositions/` |
| In-browser preview | No | **Yes** (Studio) |
| Built-in Export UI | No | **Yes** (Studio's Render button) |
| Batch / Lambda at scale | Per-widget loop | **Native** (Remotion Lambda) |
| Composition reuse | No | **Yes** (compositions are React components) |
| Determinism for CI | Best-effort (Playwright timing) | **Required by design** (frame-pure functions) |
| Workflow fit for content creator | One-off MP4 | Iterate on props live, batch personalize |

### Porting an anime.js animation to Remotion

The bridge is conceptual, not literal — Remotion is declarative (`useCurrentFrame()` is the only state), anime.js is imperative (timelines built upfront). Mapping table:

| anime.js | Remotion equivalent |
|---|---|
| `createTimeline()` | derive everything from `useCurrentFrame()` |
| `.add({ duration: 700 })` | `hopFrames = (700 / 1000) * fps` |
| `delay: 200` | offset the start frame |
| `ease: "inOutSine"` | `Easing.sin` or `Easing.bezier(...)` |
| `anime.engine.speed = 2` | render at lower duration / higher fps |
| `text.split()` + char animate | iterate chars + compute glyph per frame |
| `loop: true` | modulo on the frame counter |
| `svg.createDrawable` + `draw: 'a b'` | animate `strokeDashoffset` via `interpolate` |

Both the standalone HTML widget AND the Remotion composition can share the same data shape (nodes / edges / paths / text / etc.). The animation logic is rewritten, the content stays the same. This means a pattern's `inputs the user must provide` schema in `patterns/X-name.md` doubles as the props shape for the Remotion `<Composition>`.

## Mistakes to avoid

1. **Recording during animation auto-play** — start the timeline manually at frame 0, don't rely on auto-play timing.
2. **Wrong aspect ratio** — confirm target ratio with user before recording; redesigning a 16:9 system flow as 9:16 is significant work.
3. **VBR (variable bitrate) codecs** for short clips — leads to inconsistent frame timing. Use CFR / `-vsync cfr`.
4. **No `pix_fmt yuv420p`** — videos won't play on iOS / older browsers / some social platforms.
5. **CCapture.js without `requestAnimationFrame`** — drops frames. Always drive `step()` via rAF.
