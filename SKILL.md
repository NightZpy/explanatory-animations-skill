---
name: explanatory-animations
description: Animate explanations for any topic — system flows, lifecycles, algorithms, mechanical motion, orbits, particle systems, neural network internals, math derivations, geographic flows, and more. Use this skill when the user says "animate", "visualize", "show step by step", "ByteByteGo style", "explain X with motion", "interactive diagram", or describes a process that needs to be replayable. Asks the user about pattern, palette, typography, assets, and export before generating code.
---

Build **didactic animations** — interactive, replayable, controllable visualizations where motion teaches. Twelve patterns cover state machines, system maps, mechanical motion, orbits, particle flow, layered transformations, math derivations, geographic flows, cross-sections, and timelines. Shared visual language (palette, typography, controls strip) across every pattern.

## When this skill runs

User says any of:
- "animate / visualize this", "explain X with motion", "show me how X works step by step"
- "ByteByteGo style", "interactive diagram", "make it replayable"
- "build an animation of <topic>"

If the request looks decorative (hero animations, scroll parallax, page-load reveals), defer to the `frontend-design` skill instead.

## 5-step discovery protocol (always start here)

Before writing code, ask the user. Default to "you choose" if they say so — pick the highest-ranking match and explain why in one sentence.

**1 — Topic.** "What do you want to animate?" Skip if the request already has enough detail.

**2 — Pattern.** Show 3-4 patterns from the catalog the topic fits, with one-line previews. See [`patterns/_index.md`](./patterns/_index.md). Recommend one based on the topic.

**3 — Visual style.**
- **Palette**: propose 3 alternatives — Voltage (default), Editorial, Neon dark. Full options in [`library/colors.md`](./library/colors.md).
- **Typography**: propose 3 pairings — Geist+Geist Mono (default), Fraunces+JetBrains Mono, Space Grotesk+IBM Plex Mono. See [`library/typography.md`](./library/typography.md).
- **Icons/images**: ask whether the user (a) provides assets, (b) wants Claude to find them, or (c) accepts AI-drawn SVG. See [`library/icons.md`](./library/icons.md).

**4 — Complexity.** "How many steps / components? (4-6 digestible, 8-12 thorough, 15+ chapter it)."

**5 — Interactivity + export.** Confirm base controls (Play/Pause/Restart/Speed) are always included. Ask about extras: path selector, step-through mode, annotations, **export to video** (then resolution/fps/aspect ratio — see [`library/export.md`](./library/export.md)).

## The 3 hard rules

1. **Motion = pedagogy.** Every animated frame teaches the next idea. If removing motion doesn't hurt the explanation, remove it.
2. **One focal point at a time.** Use dim + highlight aggressively.
3. **Always replayable + controllable.** Play / Pause / Restart + speed are not optional.

If any rule is broken, redo it.

## Pattern catalog

Twelve patterns, each in its own doc under [`patterns/`](./patterns/). Pick by what's being explained:

| Code | Pattern | Use for |
|---|---|---|
| **A** | [Lifecycle / state machine](./patterns/A-lifecycle.md) | Entity progressing through states with branches |
| **B** | [System flow (ByteByteGo)](./patterns/B-system-flow.md) | Request through layered subsystems |
| **C** | [Cursor over data structure](./patterns/C-algorithm-cursor.md) | Algorithm on a visible structure |
| **D** | [Side-by-side comparison](./patterns/D-comparison.md) | Two approaches contrasted |
| **E** | [Term-by-term math reveal](./patterns/E-math-reveal.md) | Formula derived stepwise |
| **F** | [Mechanical / kinematic](./patterns/F-mechanical.md) | Physical machine, gears, pistons, pendulum |
| **G** | [Orbital / celestial](./patterns/G-orbital.md) | Bodies in orbit: solar system, atoms |
| **H** | [Particle flow](./patterns/H-particle-flow.md) | Many entities flowing along paths |
| **I** | [Layered transformation](./patterns/I-layered-transform.md) | Data through stacked layers: LLM, neural net |
| **J** | [Geographic map](./patterns/J-geographic-map.md) | Flows across real geography |
| **K** | [Cross-section / stack](./patterns/K-cross-section.md) | Literal stacked layers: OSI, memory hierarchy |
| **L** | [Timeline / sequence](./patterns/L-timeline.md) | Time-axis explanations: handshakes, signals |

Tie-breaker order: L → A → B → I → K → F → G → H → J → C → D → E.

## Shared style references

- [`library/colors.md`](./library/colors.md) — 3 palette presets + semantic tones + path colors
- [`library/typography.md`](./library/typography.md) — 3 typography pairings + role mapping
- [`library/icons.md`](./library/icons.md) — emoji vs Lucide vs custom SVG vs user-provided
- [`library/controls.md`](./library/controls.md) — controls strip spec (Play/Pause/Restart/Speed/Path/Status)
- [`library/timing.md`](./library/timing.md) — duration/delay/easing reference table
- [`library/export.md`](./library/export.md) — export-to-video pipeline (CCapture + Puppeteer + manual)

## Engine

- **Anime.js v3.2.1** loaded once via CDN with `defer`. APIs in [`engine/anime-cheatsheet.md`](./engine/anime-cheatsheet.md).
- **SVG** for geometry (not Canvas unless >1000 particles).
- **CSS Grid** for 2D layouts. **`getBoundingClientRect`** at play time for responsive arrows.
- **One library, one font set, one palette** per animation.

## Required output (every animation)

```
┌──────────────────────────────────────────────────────────────────────┐
│  ▶ Play   ⏸ Pause   ↻ Restart  │  speed [0.5×] [1×] [2×]            │
│  [path A] [path B] [path C]    │  status: playing… / paused / done  │
└──────────────────────────────────────────────────────────────────────┘
                       ┌────────────────────┐
                       │   animation stage  │
                       └────────────────────┘
```

Full spec in [`library/controls.md`](./library/controls.md).

## Quick start

For a hand-rolled widget, copy `examples/lifecycle.html` as a starting point and adapt to your pattern's needs. The example is fully self-contained (one HTML file with inlined CSS + JS, plus the anime.js CDN) — no build step required.

For each pattern, use the **Anime.js skeleton** section in its pattern doc as the reference for the timeline structure.

## Output checklist (self-grade before declaring done)

- [ ] Discovery protocol completed (topic, pattern, style, complexity, interactivity confirmed)
- [ ] Pattern explicitly chosen from the catalog (not improvised)
- [ ] 3 core rules respected (pedagogy / focal point / controllable)
- [ ] Play / Pause / Restart + correct disabled states
- [ ] Speed pill drives `window.anime.speed`, persists across path changes
- [ ] Path selector present if pattern has multiple paths
- [ ] Status indicator reaches a terminal state
- [ ] No diagonal arrows in architecture diagrams (orthogonal only)
- [ ] Edge labels have background rects for legibility
- [ ] `prefers-reduced-motion` respected
- [ ] Mobile fallback works ≤720px
- [ ] Coordinates measured at play time (not hardcoded)
- [ ] Self-contained: works without host page CSS
- [ ] If export requested: resolution + fps + aspect ratio confirmed, recording pipeline tested

Unchecked → the animation is a draft, not a deliverable.

## Common mistakes (all 10 in [`patterns/_mistakes.md`](./patterns/_mistakes.md))

Top offenders:
1. Static infographic disguised as animation (no state changes per arrival)
2. Diagonal arrows in architecture diagrams (orthogonal only)
3. Edge labels without backgrounds (illegible over the line)
4. Numbered steps inside the node cards (numbers belong on the arrows)
5. Speed control that resets between path changes
6. `anime.speed` set after `anime.timeline()` started

## Reference implementations

See [`examples/`](./examples/) — one standalone HTML per pattern, no build step. Open in a browser.

## Why this skill exists

Without it, "animate this explanation" produces: static row of emoji cards, diagonal arrows, no controls, generic Inter font, auto-play that's already over. With it, Claude produces interactive pedagogically-honest animations that match ByteByteGo / Stripe Docs / 3Blue1Brown / MDN, and **asks first** rather than guessing.
