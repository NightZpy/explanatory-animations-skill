# Content-creator uses

When the animation is for social-media content (reels / shorts / TikTok / YouTube intro / podcast clip / motion poster), the priorities shift from didactic. Use this guide instead of `controls.md` + `timing.md` for the creator case.

## Different priorities than didactic

| Aspect | Didactic | Content-creator |
|---|---|---|
| Primary goal | Teach a concept | Capture attention in 3 seconds |
| Controls | Required (Play/Pause/Restart/Speed/Path) | Often **not needed** — animation runs once for export |
| Looping | Rare (only ambient / orbital) | Common (background loops, reel intros) |
| Auto-play | After layout settles, ~250ms delay | Immediate, no delay |
| Duration | 6-15s | 1-6s (reel) or infinite loop |
| Replayability | Critical | Optional |
| Palette | Voltage default (light, technical) | Often dark mode + neon, or branded |
| Typography | Geist for accuracy | Bold, large, often custom display fonts |
| Output | HTML widget embedded in docs | Video file (MP4) for upload to platform |

## Aspect ratios

Pick before designing. Doing this right saves redrawing later.

| Target platform | Ratio | Resolution |
|---|---|---|
| TikTok / Reels / Shorts | **9:16** | 1080×1920 |
| Twitter / X video | 16:9 or 1:1 | 1920×1080 or 1080×1080 |
| Instagram feed | 1:1 or 4:5 | 1080×1080 or 1080×1350 |
| YouTube standard | 16:9 | 1920×1080 (or 3840×2160 for premium) |
| LinkedIn | 1:1 or 16:9 | 1080×1080 or 1920×1080 |
| Podcast cover anim | 1:1 | 3000×3000 (for Apple) |

For 9:16, **redesign** vertically — do not just crop a 16:9 horizontal layout. Stack content top-to-bottom; reduce horizontal text breadth.

## Hook in 3 seconds

A reel viewer decides in 1.5-3 seconds whether to scroll past. Your animation must do its key visual within that window:

1. **First 500ms**: something moves, something contrasts.
2. **1-2s**: the headline appears (full or partially revealed).
3. **3s**: the curiosity gap is established — the viewer wants the punchline.
4. **3-6s**: payoff (full reveal, final state, CTA).

Skip the slow build-up. Auto-play kicks in immediately, ideally with the most striking visual already happening.

## Common creator scenarios

### Reel/Short intro (3-5 seconds)

Best patterns: **M** (text effects), **P** (line draw with logo). Quick reveal of brand name or title.

```js
// Pattern M.1 scramble for brand reveal
import { animate, createTimeline, text, stagger, utils } from "https://esm.sh/animejs@4";
const split = text.split("h1", { chars: true, accessible: true });
const GLYPHS = "█▓▒░@#$%&*+=<>?!/X".split("");
split.chars.forEach((el, i) => {
  const seq = Array.from({length: 12}, () => utils.randomPick(GLYPHS));
  seq.push(el.dataset.final || el.textContent);
  animate(el, {
    innerHTML: seq,
    color: ["#eab308", "#22d3ee", "#fff"],
    duration: 600,
    delay: i * 25,
    ease: "steps(20)",
  });
});
```

### Counter reveal (announce a milestone)

Best pattern: **N.2** (multi-stage counter). For "10K subs", "$1M raised", "1 year together".

```js
animate(".count", {
  innerHTML: [0, 10000],
  modifier: (v) => Math.round(v).toLocaleString(),
  duration: 3000,
  ease: "cubicBezier(1,0,1,1)",
});
```

Add particle burst at the end for celebration energy (see N.6 in pattern doc).

### Talking-head background loop

Best pattern: **O.1** (drift). Behind a podcast host or interview, ambient and not distracting.

- Loop infinitely
- Low contrast against background
- No focal point — meant to be peripheral
- Slow easing (`inOutSine`, `duration: 8000-12000`)

### Sound wave / podcast audiogram

Best pattern: **P.3** (sound wave grid). 30-second clip with bars that respond to audio amplitude.

- Drive bars from WebAudio analyzer's frequency data (real)
- Or fake it with `utils.random` over time for non-reactive use
- 9:16 vertical, bars span full width

### Static thumbnail with subtle motion

Best pattern: **M.5** (wave) or **O.3** (pulse). For YouTube thumbnails — animated PNG / WebP.

- 2-3 second loop max
- Very subtle motion (5-10px translation)
- Most of the image static so the thumbnail still works as a static preview

## Production controls (different from didactic widget controls)

For social-media export, you don't ship the play/pause/restart UI — the video is the deliverable. But during *development* you want:

- **Hidden controls** for the operator to scrub, restart, export. Press `1`/`2`/`3` to switch variations. Add an "export" button that triggers CCapture.
- **Frame-perfect timeline** — drive everything through `createTimeline` so a single `tl.seek(t)` gets you to any frame.

Hide controls with `?clean=1` URL param when recording:

```js
if (new URL(location).searchParams.get("clean") === "1") {
  document.querySelectorAll(".controls").forEach(el => el.style.display = "none");
}
```

## Color palettes for content

Use the **Neon dark** preset from `colors.md` as the default for creator content — dark backgrounds let neon accents pop on dark mobile screens.

For brand-aligned, take the brand's primary color and:
- Use it as `--accent` (the focal "you are here" color)
- Build the background from a darkened brand color (mix with #0a0a0a at 90%)
- Keep text white-ish (`#f4f4f5`)
- Add ONE complementary accent (across the color wheel from primary) for path-2 / contrast

## Typography for creator content

Default to display weights that read at thumbnail scale:

| Use | Font | Weight | Size for 1080p reel |
|---|---|---|---|
| Hero headline | Geist or Space Grotesk | 700-900 | 64-96 px |
| Subhead | Geist | 500-600 | 32-42 px |
| Body / quote | Geist | 400-500 | 24-28 px |
| Mono / code / number | Geist Mono | 600-700 | varies, large |
| CTA / tag | Geist Mono uppercase | 700 + letter-spacing .12em | 14-18 px |

**Never** drop below 20px text on a 9:16 reel — readable on phones is the floor.

## Common mistakes (creator-specific)

1. **Including the controls strip in the export**. Hide with `?clean=1` before recording.
2. **Auto-play with 250ms delay**. For creator videos the timeline starts at t=0 of the recording — no delay.
3. **Looping a one-shot reveal**. If the punchline is "BIG NUMBER appears", make it run once and freeze, not loop.
4. **Static for the first 1.5 seconds**. Viewers scroll. Open with motion.
5. **Text too small for thumbnail**. Test by zooming the recording out to 200×200px. Can you still read the headline?
6. **Aspect ratio 16:9 used for TikTok**. The mobile crop will eat 40% of your composition.
7. **No safe zone for platform UI**. TikTok's UI covers the bottom 25% of the screen. Keep titles in the top 60%.
8. **Background music conflicts with the visual rhythm**. Sync key beats of the animation to the audio (export silent first, then layer music with `ffmpeg amix`).

## Export workflow (recap from library/export.md)

1. Build the widget with controls hidden via `?clean=1`.
2. Use CCapture for in-browser recording, or Puppeteer for headless automation.
3. Output WebM → re-encode to MP4 with H.264 + `pix_fmt yuv420p` for max compatibility.
4. Add audio with `ffmpeg amix` if needed.
5. For 9:16: render at 1080×1920, framerate 30 or 60 fps.

Full pipelines in [`library/export.md`](./export.md).

## Where this skill fits in the creator workflow

```
[Brief]  →  Pick pattern (M/N/O/P)  →  Pick style preset  →
            Generate widget with `?clean=1`  →
            Record via CCapture / Puppeteer  →
            Add audio in ffmpeg  →
            Upload to platform
```

If the user doesn't know their brief yet (still in ideation), pull them back to the **5-step discovery protocol** in `SKILL.md`. Don't generate before the protocol completes — half-described content animations are wasted effort.
