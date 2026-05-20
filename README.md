# explanatory-animations

A Claude skill for building **didactic animations** — interactive, replayable, controllable visualizations that explain a concept, lifecycle, algorithm, mechanical system, orbital motion, particle flow, LLM internals, math derivation, geographic flow, or anything else that benefits from motion.

Designed to match the visual quality of **ByteByteGo / Stripe Docs / 3Blue1Brown / MDN**, with a shared visual language (palette, typography, controls) across 12 distinct patterns.

The skill asks the user **before** generating code: topic, pattern, palette, typography, asset strategy, complexity, interactivity, and export needs. Then it produces a self-contained widget — one HTML file, one `<script>` tag, no build step.

## What's in this skill

```
explanatory-animations/
├── SKILL.md                       # entry point — discovery protocol + pattern index
├── README.md                      # this file
├── LICENSE                        # MIT
├── patterns/                      # 16 deep-dive pattern docs + index + mistakes
│   ├── _index.md
│   ├── _mistakes.md
│   ├── A-lifecycle.md             # state machines with branches
│   ├── B-system-flow.md           # ByteByteGo-style architecture
│   ├── C-algorithm-cursor.md      # sorting, search, traversal
│   ├── D-comparison.md            # before/after, A/B
│   ├── E-math-reveal.md           # formula derivations
│   ├── F-mechanical.md            # engines, gears, pendulum
│   ├── G-orbital.md               # solar system, atoms
│   ├── H-particle-flow.md         # data flow, traffic, electrons
│   ├── I-layered-transform.md     # LLM, neural net, compiler stages
│   ├── J-geographic-map.md        # regional flows, supply chain
│   ├── K-cross-section.md         # OSI, memory hierarchy, strata
│   ├── L-timeline.md              # SSL handshake, OAuth, signal timing
│   ├── M-text-effects.md          # scramble / split / type-on / magnet / wave
│   ├── N-counter.md               # big-number reveals, flip-clock, KPI cards
│   ├── O-shape-morph.md           # drift, polygon morph, generative bg loops
│   └── P-svg-line-drawing.md      # sound waves, sonar, route reveals, signatures
├── library/                       # shared style references
│   ├── colors.md                  # 4 palette presets + semantic tones + path colors
│   ├── typography.md              # 3 typography pairings + role mapping
│   ├── icons.md                   # emoji vs Lucide vs custom SVG vs user assets
│   ├── controls.md                # Play/Pause/Restart/Speed/Path/Status strip
│   ├── timing.md                  # duration + easing reference
│   ├── export.md                  # 3 video export pipelines (manual / CCapture / Puppeteer)
│   └── content-creator-uses.md    # priorities for reel/shorts/podcast — different from didactic
├── engine/
│   └── anime-cheatsheet.md        # Anime.js v4 APIs + v3 → v4 migration table
└── examples/
    ├── lifecycle.html             # Pattern A reference (v4)
    ├── system-flow.html           # Pattern B reference (v4)
    ├── text-scramble.html         # Pattern M reference (v4)
    ├── counter-stars.html         # Pattern N reference (v4)
    ├── shape-drift.html           # Pattern O reference (v4)
    └── sound-wave.html            # Pattern P reference (v4)
```

## How Claude uses it

1. **User says** "animate this", "visualize X", "ByteByteGo style", "show step by step", etc.
2. **Claude runs the discovery protocol** (5 quick questions: topic, pattern, style, complexity, interactivity).
3. **User answers**, or says "you choose" for any step.
4. **Claude picks the pattern** from the catalog of 12, references the relevant pattern doc + style libraries.
5. **Claude generates** a self-contained HTML widget with controls, anime.js animations, and the right palette/typography/icons.

## Install

### Personal (recommended — available across all your projects)

```bash
git clone https://github.com/<you>/explanatory-animations-skill.git \
  ~/Documents/projects/claude/skills/explanatory-animations

ln -s ~/Documents/projects/claude/skills/explanatory-animations \
      ~/.claude/skills/explanatory-animations
```

After Claude Code picks up the symlink (live or next session), verify with `/skills` — `explanatory-animations` should appear in the list.

### Per-project (committed to a repo)

```bash
mkdir -p .claude/skills
git submodule add https://github.com/<you>/explanatory-animations-skill.git \
  .claude/skills/explanatory-animations
```

## Invoke

When you (or Claude itself) detect a request like:

- "animate this flow"
- "ByteByteGo style"
- "make an interactive diagram of X"
- "explain X visually"
- "walk me through how X works step by step"

…Claude auto-invokes the skill (matched against the `description` in SKILL.md). You can also invoke it explicitly via `/explanatory-animations` or by including the phrase "using the explanatory-animations skill" in your prompt.

## Patterns at a glance

**Family 1 — Didactic (teach a concept)**

| Code | Best for |
|---|---|
| **A** Lifecycle | Job lifecycle, order status, ticket state |
| **B** System flow | Request through CDN/app/DB layers (ByteByteGo) |
| **C** Cursor | Sorting / search / traversal algorithms |
| **D** Comparison | A vs B (with/without cache, monolith vs micro) |
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

## Style consistency

Every pattern shares:

- **Color palette** — 3 presets (Voltage / Editorial / Neon dark) + brand-aligned option
- **Typography** — 3 pairings (Geist / Fraunces / Space Grotesk) all with mono fallback
- **Controls strip** — Play / Pause / Restart / Speed pill / Path selector / Status
- **Accessibility** — `prefers-reduced-motion`, keyboard nav, screen-reader roles
- **Mobile fallback** — ≤720px gracefully degrades

So all your animations look like they belong to the same publication, regardless of which pattern each one uses.

## Why a skill?

Without it, "animate this explanation" produces a static row of emoji cards with a dot, diagonal arrows that look like a UML draft, no controls, generic Inter font. With it, Claude produces real interactive pedagogically-honest animations — and **asks first** instead of guessing.

## Companion skills

- **`frontend-design`** — for decorative motion (hero animations, scroll parallax). Use that one when motion is for *delight*, this one when motion is for *teaching*.
- **`docx-comments`**, **`excalidraw`** — other content-focused skills.

## License

MIT. See [`LICENSE`](./LICENSE).

## Roadmap

- [ ] Reference implementations for patterns C–L
- [ ] `scripts/generate-widget.py` — generate a complete widget HTML from a YAML config (pattern + content data)
- [ ] Video export script with sensible defaults (1080p / 60fps / mp4, `?clean=1` headless mode)
- [ ] Storybook-style demo page indexing all reference implementations
- [ ] Brand-aligned palette generator (input: brand hex → output: full token set)
- [ ] Pattern Q — Network graph (force-directed, for explaining graph algorithms / social networks)
- [ ] Pattern R — 3D / isometric (CSS 3D transforms for explanations that need depth)

## Contribute

If you add a new pattern, follow the existing structure:

1. Add an entry in [`patterns/_index.md`](./patterns/_index.md) and [`SKILL.md`](./SKILL.md) → "Pattern catalog"
2. Create `patterns/<letter>-<name>.md` using the same sections as the existing pattern docs
3. Add a reference implementation in `examples/`
4. Submit a PR with a 1-paragraph description of when to use the new pattern vs the existing ones
