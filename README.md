# explanatory-animations

A **Claude Code plugin** for building **didactic animations** + **content-creator effects** — interactive, replayable, controllable visualizations that explain a concept (lifecycle, algorithm, mechanical / orbital motion, LLM internals, math derivation, geographic flow, etc.) or capture attention on social media (scramble text, big-number counters, shape morphing, SVG line drawing, sound waves).

Designed to match the visual quality of **ByteByteGo / Stripe Docs / 3Blue1Brown / MDN**, with a shared visual language (palette, typography, controls) across **16 patterns**.

## Install

This repo is a **Claude Code plugin** (with `.claude-plugin/plugin.json` manifest), so it installs via Claude's plugin manager. Two ways:

### Via marketplace (one-time setup, recommended)

```
/plugin marketplace add NightZpy/explanatory-animations-skill
/plugin install explanatory-animations
```

Updates land automatically when `version` in `plugin.json` is bumped. Run `/plugin list` to verify.

### Direct from this repo

Without going through a marketplace:

```bash
# Clone into a stable location (anywhere)
git clone https://github.com/NightZpy/explanatory-animations-skill.git ~/dev/explanatory-animations-skill

# Tell Claude Code about it for the current session
claude --plugin-dir ~/dev/explanatory-animations-skill
```

For a one-off session without persisting the install, use `--plugin-dir` only for that launch.

### Standalone-skill mode (no plugin manager)

The `main` branch ships the same content as a **standalone skill** (no manifest, no namespacing) for users who prefer `git clone ~/.claude/skills/`. Switch branches if you want that flavor:

```bash
git clone -b main https://github.com/NightZpy/explanatory-animations-skill.git \
  ~/.claude/skills/explanatory-animations
```

After install, the plugin exposes:

| What | How to invoke |
|---|---|
| Main skill | `/explanatory-animations:animate` (or just describe what you want — auto-invokes) |

## How Claude uses it

1. **User says** "animate this", "visualize X", "ByteByteGo style", "explica con animación cómo funciona…", "make a scramble text reveal", "counter going up to 50K", etc.
2. **Claude runs the discovery protocol** (5 quick questions: topic, pattern, style, complexity, interactivity).
3. **User answers**, or says "you choose" for any step.
4. **Claude picks one of 16 patterns** and reads the relevant `patterns/X-name.md` + style library refs.
5. **Claude generates** a self-contained HTML widget. Then delivers either:
   - **A preview URL** via `scripts/render.py` (auto-bootstraps deps in `~/.cache/`), OR
   - **An MP4 file** via the same script in `--out` mode, OR
   - **Embeds a `widget-helpers/export-button.js`** so the user can click Export in the browser themselves and download WebM, OR
   - **Generates a Remotion `<Composition>`** under `scripts/export-remotion/` for in-Studio preview + Render button (when batch / personalized rendering is needed).

## What's in this plugin

```
explanatory-animations-skill/                ← plugin root
├── .claude-plugin/
│   └── plugin.json                          ← plugin manifest
├── README.md                                ← this file
├── LICENSE                                  ← MIT
└── skills/
    └── animate/                             ← the skill (only one for now)
        ├── SKILL.md                         ← entry point — discovery + index
        ├── patterns/                        ← 16 deep-dive pattern docs + index + mistakes
        │   ├── A-lifecycle.md   ... L-timeline.md      (12 didactic)
        │   └── M-text-effects.md  ... P-svg-line-drawing.md   (4 creator)
        ├── library/                         ← shared style references
        │   ├── colors.md, typography.md, icons.md
        │   ├── controls.md, timing.md, export.md
        │   └── content-creator-uses.md
        ├── engine/
        │   └── anime-cheatsheet.md          ← Anime.js v4 APIs + v3→v4 migration
        ├── widget-helpers/
        │   └── export-button.js             ← drop-in Export button (any widget)
        ├── scripts/
        │   ├── render.py                    ← autonomous renderer (preview URL or MP4)
        │   ├── export-widget.py             ← alias → render.py
        │   └── export-remotion/             ← React + Remotion Studio
        └── examples/
            ├── lifecycle.html, system-flow.html
            ├── text-scramble.html, counter-stars.html
            ├── shape-drift.html, sound-wave.html
            └── README.md
```

> **Single skill, multiple delivery surfaces.** This plugin currently ships one skill (`animate`). The architecture supports adding more in `skills/<name>/SKILL.md` — e.g. an `export` skill that triggers only when the user wants to record an already-open widget, or a `from-spec` skill that takes a YAML config and generates the widget without the discovery dialogue. Those are roadmap items.

## Patterns at a glance

**Family 1 — Didactic (teach a concept)**

| Code | Best for |
|---|---|
| **A** Lifecycle | Job lifecycle, order status, ticket state |
| **B** System flow | Request through CDN / app / DB layers (ByteByteGo) |
| **C** Cursor | Sorting / search / traversal algorithms |
| **D** Comparison | A vs B (with / without cache, monolith vs micro) |
| **E** Math reveal | Formula derived term-by-term |
| **F** Mechanical | Engines, gears, pumps, clocks |
| **G** Orbital | Solar system, atomic shells |
| **H** Particle flow | Data flowing through wires, traffic, electrons |
| **I** Layered transform | LLM internals, neural net, compiler stages |
| **J** Geographic | Regional request flow, supply chain, migration |
| **K** Cross-section | OSI 7 layers, memory hierarchy, strata |
| **L** Timeline | TLS handshake, OAuth, signal timing |

**Family 2 — Content creator (capture attention)**

| Code | Best for |
|---|---|
| **M** Text effects | Reel intros, scramble headlines, magnet on hover, CTA reveal |
| **N** Counter / clock | 10K / $1M / 50K star reveal, flip-digit clock, KPI dashboard |
| **O** Shape morph | Generative background loops, podcast intro motion, ambient bg |
| **P** SVG line drawing | Sound waves, sonar pings, logo reveal, route trace |

## Export pipeline (6 strategies)

The skill ships a layered export system — pick the right one for the use case. Full details in `skills/animate/library/export.md`.

| Strategy | When to use |
|---|---|
| **0 — In-widget Export button** | User is in the browser, clicks "⬇ Export" → WebM in Downloads/. Works with ANY pattern. |
| **1 — Autonomous `render.py`** | Agent delivers URL or MP4 to user. Auto-bootstraps Playwright + ffmpeg in `~/.cache/`. |
| **2 — Manual screen recording** | Quick one-off, no setup. |
| **3 — Raw CCapture.js** | Hand-rolled in-browser recording with custom timing. |
| **4 — Puppeteer headless** | Custom Node + Puppeteer CI pipeline. |
| **5 — Remotion** | React Studio with live preview + props panel + Render button + Lambda batch. |

## Style consistency

Every pattern shares:

- **Color palette** — 3 presets (Voltage / Editorial / Neon dark) + brand-aligned option
- **Typography** — 3 pairings (Geist / Fraunces / Space Grotesk) all with mono fallback
- **Controls strip** — Play / Pause / Restart / Speed pill / Path selector / Status
- **Accessibility** — `prefers-reduced-motion`, keyboard nav, screen-reader roles
- **Mobile fallback** — ≤720px gracefully degrades

So all animations look like they belong to the same publication, regardless of pattern.

## Why a plugin (not just a skill)?

Without it, asking Claude to "animate this explanation" produces: static row of emoji cards with a dot, diagonal arrows that look like a UML draft, no controls, generic Inter font, auto-play that's already over. With it, Claude produces real interactive pedagogically-honest animations — and **asks first** instead of guessing.

The plugin layout (vs a standalone skill in `~/.claude/skills/`) gives:

- **Versioned releases** — `version` in `plugin.json` controls when users see updates.
- **`/plugin install` UX** — no manual `git clone` paths to memorize.
- **Marketplace distribution** — submit to `anthropics/claude-plugins-community` for one-line discovery.
- **Future skills** — easy to add `skills/export/` or `skills/from-spec/` siblings.
- **Namespacing** — `/explanatory-animations:animate` won't conflict with another `animate` skill.

## Companion skills

- **`frontend-design`** — for decorative motion (hero animations, scroll parallax). Use that one when motion is for *delight*, this one when motion is for *teaching* or *content creation*.

## License

MIT. See `LICENSE`.

## Roadmap

- [ ] Reference implementations for patterns C–L
- [ ] `scripts/generate-widget.py` — generate complete widget HTML from a YAML config
- [ ] `scripts/render.py --convert <webm>` subcommand (WebM → MP4 via bundled ffmpeg)
- [ ] Brand-aligned palette generator (input: brand hex → output: full token set)
- [ ] Submit to `anthropics/claude-plugins-community` marketplace
- [ ] Pattern Q — Network graph (force-directed)
- [ ] Pattern R — 3D / isometric (CSS 3D transforms)
- [ ] Second skill `skills/export/` for widget-already-open recording-only flow

## Contribute

If you add a new pattern, follow the existing structure:

1. Add an entry in `skills/animate/patterns/_index.md` and `skills/animate/SKILL.md` → "Pattern catalog"
2. Create `skills/animate/patterns/<letter>-<name>.md` using the same sections as existing pattern docs
3. (optional) Add a reference implementation in `skills/animate/examples/`
4. Submit a PR with a 1-paragraph description of when to use the new pattern vs the existing ones
