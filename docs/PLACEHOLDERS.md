# Visual assets — what to drop where

When you have GIFs / screenshots / videos ready, place them under `docs/` and uncomment the corresponding block in `README.md`. The README has commented-out `<!-- ![alt](docs/...) -->` lines next to each `TODO:` block that mark exactly where each asset goes.

## Required assets (in priority order)

| File path | Purpose | Aspect / format | Where it appears |
|---|---|---|---|
| `docs/hero.gif` | 8–12 sec hero demo: full agent flow (user prompt → discovery → widget → MP4 delivered) | 16:9 or 21:9 GIF (or `.mp4` via HTML5 `<video>`) | Top of README, right under the badges |
| `docs/gallery/A.gif` | Pattern A demo (lifecycle state machine) | Square or 16:9, 4-6 sec loop | "Pattern catalog" section (2×2 grid) |
| `docs/gallery/B.gif` | Pattern B demo (system flow) | Same | Same |
| `docs/gallery/M.gif` | Pattern M demo (text scramble) | Same | Same |
| `docs/gallery/P.gif` | Pattern P demo (sound wave) | Same | Same |
| `docs/flow-diagram.png` | Interaction flow sketch (agent ↔ user back-and-forth) | Any, ~1200px wide | "How it works in one minute" section |
| `docs/export-button.gif` | 8-sec GIF of the in-widget Export button flow | 16:9, shows the modal + progress bar + WebM landing | "Export pipeline" section |
| `docs/examples-thumb.png` + `docs/examples-walkthrough.mp4` (or YouTube link) | 30–60 sec walkthrough of the 6 reference examples | Up to you | "Examples" section |

## Optional but nice

| File path | Purpose |
|---|---|
| `docs/marketplace-card.png` | Custom image for the marketplace listing (Anthropic may accept it) |
| `docs/discovery-protocol.gif` | Walkthrough of the 5-step discovery dialogue |
| `docs/remotion-studio.png` | Screenshot of Remotion Studio with one of the compositions loaded |
| `docs/doctor-output.png` | Screenshot of `doctor.py` reporting `NEEDS_BOOTSTRAP` with the breakdown |
| `docs/multi-language.gif` | Same prompt in EN and ES producing the same widget |

## How to uncomment in README.md

Each placeholder block looks like:

```markdown
<!-- ─── HERO DEMO ─────────────────────────────────────────────────────────
TODO: drop a 8-12 second hero GIF here ...
────────────────────────────────────────────────────────────────────────-->

<!-- ![hero demo](docs/hero.gif) -->
```

To activate it, remove the `<!--` and `-->` from the `![hero demo](docs/hero.gif)` line. Leave the TODO comment as is (or delete it).

## Recording tips

- **Hero GIF**: capture at 1080p, save as `.gif` (under 10 MB) or `.mp4` (under 5 MB). Use `ffmpeg -i in.mp4 -vf "fps=15,scale=1080:-1:flags=lanczos,palettegen" palette.png` then `ffmpeg -i in.mp4 -i palette.png -lavfi "fps=15,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" hero.gif`.
- **Pattern demos**: each pattern's reference example HTML already loops cleanly — just record one cycle at 1×.
- **Export button demo**: open `examples/lifecycle.html`, click the ⬇ Export button, pick options, watch the modal + progress bar. Record from the click forward.

## License of assets

If you produce the assets yourself, MIT applies. If you reuse third-party visuals, document attribution in each file's metadata or in this file.
