# explanatory-animations

[![Validate](https://github.com/NightZpy/explanatory-animations-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/NightZpy/explanatory-animations-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Plugin: Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-orange)](https://github.com/anthropics/claude-plugins-community)
[![Version](https://img.shields.io/badge/version-0.4.0-green)](CHANGELOG.md)

> A [Claude Code](https://code.claude.com) plugin for building **polished interactive animated explanations** and **content-creator effects** in your browser — 16 patterns covering didactic visualizations (ByteByteGo-style system flows, lifecycles, algorithms, mechanical motion, LLM internals, math derivations, geographic maps, …) and creator effects (scramble text, big-number counters, shape morphing, SVG line drawing). Auto-installs, runs locally, exports to MP4 with one command.

![hero demo][hero-demo]

---

## What it does

Ask Claude in plain English (or Spanish) to animate something — a system architecture, an algorithm, a workflow, a piece of math, a content-creator reel — and the plugin produces a self-contained interactive HTML widget. From there you can:

- **Watch + replay it in the browser** with built-in Play / Pause / Restart / Speed controls.
- **Click "⬇ Export"** in the widget to record a WebM directly in the browser.
- **Get an MP4** from Claude by asking for the output as video — the agent handles render and delivery autonomously.
- **Use Remotion Studio** for a richer preview + Render UI (live props panel, programmatic rendering, Lambda batch).

The plugin runs the **5-step discovery protocol** before generating anything — confirming topic, pattern, palette/typography/icons, complexity, and export needs — so the output matches what you actually wanted. Works in any language.

### Pattern gallery

| Pattern A — Lifecycle | Pattern B — System flow |
|---|---|
| ![Pattern A][pattern-a] | ![Pattern B][pattern-b] |
| Pattern M — Text scramble | Pattern P — Sound wave |
| ![Pattern M][pattern-m] | ![Pattern P][pattern-p] |

📺 **Full walkthrough video:** [Watch on YouTube][demo-video]

## Install

Three install paths:

### A · Via the official Claude community marketplace (planned)

Once approved into [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community):

```
/plugin marketplace add anthropics/claude-plugins-community
/plugin install explanatory-animations@claude-community
```

### B · Direct from this repo (works today)

```
/plugin marketplace add NightZpy/explanatory-animations-skill
/plugin install explanatory-animations
```

### C · Local development with `--plugin-dir`

```bash
git clone https://github.com/NightZpy/explanatory-animations-skill.git
cd explanatory-animations-skill
claude --plugin-dir .
```

After install, the plugin exposes 5 namespaced skills under `/`:

```
/explanatory-animations:animate              full flow (discovery → build → deliver)
/explanatory-animations:pick-pattern         help me choose which of 16 patterns fits
/explanatory-animations:build-widget         pattern + content → HTML widget (no export)
/explanatory-animations:export-widget        widget HTML → MP4 or preview URL
/explanatory-animations:add-export-button    inject the Export button into existing widget
```

Or just describe what you want — the plugin auto-invokes based on semantic intent, in any language.

## How it works in one minute

![interaction flow][flow-diagram]

1. **You ask** — *"animate how a request flows through our CDN"* / *"make me a scramble-text intro for a reel"* / *"show the OSI 7 layers as a stack"* / *"explica con animación el sistema solar"*.
2. **Claude runs the 5-step discovery protocol** — confirms topic, recommends a pattern, asks about palette / typography / icons / aspect ratio / export.
3. **Claude generates an HTML widget** — self-contained, no build step, loads [Anime.js v4](https://animejs.com) from `esm.sh` + Google Fonts.
4. **Claude delivers the result** — either a `localhost` URL it opens in your browser, or an MP4 file in `/tmp/`. The agent invokes `scripts/render.py` which auto-bootstraps Playwright + Chromium + ffmpeg in `~/.cache/explanatory-animations/` on the first run only (with explicit consent + a transparent breakdown of what's about to download).
5. **You watch + share** — the widget has built-in controls (Play / Pause / Restart / Speed / optional path selector / status). The optional in-widget **⬇ Export** button records WebM directly from the browser. The optional **Remotion** companion gives you a Studio with live props panel + Render button.

## Pattern catalog (16 patterns)

**Family 1 — Didactic (teach a concept)**

| Code | Pattern | Best for | Doc |
|---|---|---|---|
| **A** | Lifecycle / state machine | Job lifecycle, order status, ticket state | [doc](skills/animate/patterns/A-lifecycle.md) |
| **B** | System flow (ByteByteGo) | Request through layered subsystems | [doc](skills/animate/patterns/B-system-flow.md) |
| **C** | Cursor over data structure | Sorting / search / traversal algorithms | [doc](skills/animate/patterns/C-algorithm-cursor.md) |
| **D** | Side-by-side comparison | A vs B (with/without cache, monolith vs micro) | [doc](skills/animate/patterns/D-comparison.md) |
| **E** | Term-by-term math reveal | Formula derived stepwise | [doc](skills/animate/patterns/E-math-reveal.md) |
| **F** | Mechanical / kinematic | Engines, gears, pendulum | [doc](skills/animate/patterns/F-mechanical.md) |
| **G** | Orbital / celestial | Solar system, atoms | [doc](skills/animate/patterns/G-orbital.md) |
| **H** | Particle flow | Data flow, traffic, electrons | [doc](skills/animate/patterns/H-particle-flow.md) |
| **I** | Layered transformation | LLM internals, neural net, compiler stages | [doc](skills/animate/patterns/I-layered-transform.md) |
| **J** | Geographic map | Regional flows, supply chain | [doc](skills/animate/patterns/J-geographic-map.md) |
| **K** | Cross-section / stack | OSI 7 layers, memory hierarchy, strata | [doc](skills/animate/patterns/K-cross-section.md) |
| **L** | Timeline / sequence | TLS handshake, OAuth, signal timing | [doc](skills/animate/patterns/L-timeline.md) |

**Family 2 — Content creator (capture attention)**

| Code | Pattern | Best for | Doc |
|---|---|---|---|
| **M** | Text effects | Reel intros, scramble headlines, magnet on hover, CTA reveal | [doc](skills/animate/patterns/M-text-effects.md) |
| **N** | Numeric counter / clock | 10K / $1M / 50K star reveal, flip-digit clock, KPI dashboard | [doc](skills/animate/patterns/N-counter.md) |
| **O** | Shape morph / layered transforms | Generative loops, podcast intros, ambient backgrounds | [doc](skills/animate/patterns/O-shape-morph.md) |
| **P** | SVG line drawing | Sound waves, sonar pings, logo reveal, route trace | [doc](skills/animate/patterns/P-svg-line-drawing.md) |

Tie-breaker order: **L → A → B → I → K → F → G → H → J → C → D → E**.

## Style consistency

Every pattern shares one visual language:

- **Palette** — 3 presets (Voltage / Editorial / Neon dark) + brand-aligned option. See [`library/colors.md`](skills/animate/library/colors.md).
- **Typography** — 3 pairings (Geist+Geist Mono / Fraunces+JetBrains Mono / Space Grotesk+IBM Plex Mono) — never Arial / Inter / Roboto. See [`library/typography.md`](skills/animate/library/typography.md).
- **Iconography** — emoji (default) / Lucide / custom SVG / user-provided assets. See [`library/icons.md`](skills/animate/library/icons.md).
- **Controls strip** — Play / Pause / Restart / Speed pill / optional Path selector / Status indicator. See [`library/controls.md`](skills/animate/library/controls.md).
- **Timing reference** — duration + easing per pattern. See [`library/timing.md`](skills/animate/library/timing.md).
- **Accessibility** — `prefers-reduced-motion`, keyboard nav, screen-reader roles, mobile ≤720px graceful degrade.

## Export pipeline (6 strategies)

![export button demo][export-demo]

Full details in [`skills/animate/library/export.md`](skills/animate/library/export.md). Quick chooser:

| You want… | Strategy |
|---|---|
| **In-browser "⬇ Export" button** the user clicks → WebM downloads. Works with ANY pattern. | **0 — In-widget button** (`widget-helpers/export-button.js`) |
| **Agent delivers a URL or MP4 file** to the user with zero setup. Auto-bootstraps deps in `~/.cache/`. | **1 — `scripts/render.py`** |
| Quick one-off demo from screen | **2 — Manual screen recording** |
| Hand-rolled in-browser recording with custom timing | **3 — CCapture.js (raw)** |
| Custom Node + Puppeteer CI pipeline | **4 — Puppeteer headless** |
| **Studio with live preview + Render button + props panel + Lambda batch** | **5 — Remotion** (`scripts/export-remotion/`) |

## First-time setup (what the plugin downloads)

The plugin is transparent about installs. The first time you ask for an MP4, the agent runs `scripts/doctor.py` and shows you what's about to happen before downloading anything:

```
Para exportar este widget necesito instalar:
  • Playwright (~50 MB pip wheel)
  • Chromium (~150 MB)
  • ffmpeg: tu sistema ya lo tiene, lo reuso (skip 25 MB de download)

Todo va a ~/.cache/explanatory-animations/ — aislado de tu sistema.
Future runs reuse this cache (<200ms cold start).
Continúo? (la próxima vez ya no te pregunto)
```

Run the doctor manually any time:

```bash
python3 ~/.claude/plugins/explanatory-animations/skills/animate/scripts/doctor.py
# → JSON report on stdout, human summary on stderr
```

The cache lives at `~/.cache/explanatory-animations/`. To uninstall, delete that directory + `/plugin uninstall explanatory-animations`.

## Examples

Six standalone reference implementations under [`skills/animate/examples/`](skills/animate/examples/). Open any `.html` file directly in a browser — no build step.

| File | Pattern | What it demos |
|---|---|---|
| `lifecycle.html` | A | Branching state machine with happy / failure / retry paths |
| `system-flow.html` | B | 2D architecture with boundary regions, orthogonal arrows, numbered step badges, glowing packet |
| `text-scramble.html` | M | Four effect variants on one headline: scramble / cascade / wave / magnet |
| `counter-stars.html` | N | 50K star counter with multi-stage easing + particle burst |
| `shape-drift.html` | O | Layered SVG shapes with randomized keyframes — generative background |
| `sound-wave.html` | P | 80 vertical lines + 40 concentric circles drawing themselves — sonar / radio visualizer |

📺 **Examples walkthrough video:** [Watch on YouTube][examples-video]

## FAQ

**Q: ¿Funciona en español?**
Sí. El plugin se invoca por intención semántica, no por keywords literales. *"explica con animación cómo funciona la plataforma"*, *"hacéme un video animado de cómo funciona X"*, *"muestra el flujo paso a paso"* — todo dispara el plugin.

**Q: Do I need Node.js to use this?**
No. The autonomous renderer (`render.py`) is Python-only and bundles ffmpeg via `imageio-ffmpeg`. Only the **Remotion** export strategy (#5) needs Node — and it's optional.

**Q: How big is the first-time install?**
~175–200 MB into `~/.cache/explanatory-animations/`: Playwright (~50 MB) + Chromium (~150 MB) + ffmpeg (~25 MB if your system doesn't already have it). The agent shows this breakdown before downloading anything.

**Q: Is the cache portable / shareable?**
The cache is per-machine. To migrate a setup, copy `~/.cache/explanatory-animations/` to the new machine and the second run skips bootstrap.

**Q: Why Anime.js v4 specifically?**
v4 ships first-class primitives the patterns rely on: `text.split()` for character-level animation (Pattern M), `svg.createDrawable()` for line drawing (Pattern P), parametric easings (`inOut(N)` / `out(N)`), and `createSpring()` for mechanical patterns. It's ~14 KB gzipped, MIT-licensed, and works without a build step.

**Q: Can I use this commercially?**
Yes — MIT license. The third-party libs used (Anime.js MIT, Playwright Apache 2.0, ffmpeg LGPL/GPL with the imageio-ffmpeg LGPL build, html2canvas MIT, CCapture.js MIT, Remotion EULA — paid for companies ≥4 people) have their own terms; Strategies 0/1 are fully free for any use.

**Q: ¿Qué pasa si el render falla?**
`render.py` deja un mensaje claro en stderr y exit code distinto de cero. La cache de `~/.cache/` queda intacta — un retry no re-instala. El JSON output incluye el error path para diagnóstico.

**Q: How do I add my own pattern (Q, R, …)?**
See [`CONTRIBUTING.md`](CONTRIBUTING.md). It's additive: drop a `Q-<name>.md` in `patterns/`, add a row to the index + main SKILL.md, optionally an example, bump version, PR.

## Roadmap

- [ ] Reference implementations for patterns C–L (currently only A / B / M / N / O / P have one)
- [ ] `scripts/render.py --convert <webm>` subcommand (WebM → MP4 via bundled ffmpeg)
- [ ] Brand-aligned palette generator (input: brand hex → output: full token set)
- [ ] Pattern Q — Network graph (force-directed)
- [ ] Pattern R — 3D / isometric (CSS 3D transforms)
- [ ] Port patterns B / C / I / L / N to Remotion compositions
- [ ] Submit to `anthropics/claude-plugins-community` marketplace

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports + feature requests via [issues](https://github.com/NightZpy/explanatory-animations-skill/issues/new/choose).

## Companion skills

- **`frontend-design`** (separate plugin) — for decorative motion (hero animations, scroll parallax, decorative micro-interactions). Use that when motion is for *delight*, this plugin when motion is for *teaching* or *content creation*.

## License

MIT. See [LICENSE](LICENSE).

## Credits

Built on top of [Anime.js v4](https://animejs.com) (Julian Garnier, MIT), [Playwright](https://playwright.dev) (Microsoft, Apache 2.0), [html2canvas](https://html2canvas.hertzen.com) (Niklas von Hertzen, MIT), [CCapture.js](https://github.com/spite/ccapture.js) (Jaume Sánchez, MIT), [Remotion](https://www.remotion.dev) (Remotion GmbH, custom EULA), and [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) (LGPL ffmpeg build).

<!--
─────────────────────────────────────────────────────────────────────────────
 VISUAL ASSETS — replace the paths/URLs below with your real ones.
 Until each file exists, GitHub shows the alt text + a broken-image icon.
 Suggested sources:
   · Record GIFs locally → drop in docs/ → commit
   · Upload videos to YouTube → replace the placeholder URLs below
─────────────────────────────────────────────────────────────────────────────
-->
[hero-demo]:      docs/hero.gif                     "Replace with 8–12s hero GIF (16:9 or 21:9): full agent flow user→discovery→widget→MP4"
[pattern-a]:      docs/gallery/A.gif                "Replace with 4–6s loop of Pattern A reference example"
[pattern-b]:      docs/gallery/B.gif                "Replace with 4–6s loop of Pattern B reference example"
[pattern-m]:      docs/gallery/M.gif                "Replace with 4–6s loop of Pattern M reference example"
[pattern-p]:      docs/gallery/P.gif                "Replace with 4–6s loop of Pattern P reference example"
[flow-diagram]:   docs/flow-diagram.png             "Replace with sketch / screenshot of the agent ↔ user back-and-forth"
[export-demo]:    docs/export-button.gif            "Replace with 8s GIF: click ⬇ Export → modal → progress → WebM download"
[demo-video]:     https://youtu.be/REPLACE_ME_HERO  "Replace with full walkthrough YouTube URL"
[examples-video]: https://youtu.be/REPLACE_ME_EXAMPLES  "Replace with 30–60s YouTube URL of the 6 reference examples"
