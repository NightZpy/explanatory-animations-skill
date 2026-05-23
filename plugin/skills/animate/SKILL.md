---
name: explanatory-animations
description: USE THIS SKILL whenever the user wants to animate, visualize, or explain something with motion — architecture / platform / system flows, lifecycles, algorithms, mechanical or orbital motion, particle systems, LLM internals, math derivations, geographic flows, or content-creator effects (scramble text, big-number counters, shape morph, SVG line drawing, sound waves). Produces a self-contained interactive HTML widget (Anime.js v4 + SVG, replayable, controllable, exportable to video). Runs a 5-step discovery (topic, pattern, style, complexity, export) and picks one of 16 patterns. Prefer this over generic brainstorming whenever the user already wants an ANIMATED explanation rather than to ideate. Works in any language — invoke based on user intent, not literal keywords.
---

Build **interactive animations** — replayable, controllable visualizations that either **teach a concept** (didactic) or **capture attention on social media** (creator-focused). Sixteen patterns share one visual language (palette / typography / controls strip).

**Engine:** Anime.js **v4** (`v4.1.x`). API is **incompatible with v3** — use `animate()`, `createTimeline()`, named imports, `ease` not `easing`. Full reference in [`engine/anime-cheatsheet.md`](./engine/anime-cheatsheet.md).

## When this skill runs

User says any of:
- "animate / visualize this", "explain X with motion", "show me how X works step by step"
- "ByteByteGo style", "interactive diagram", "make it replayable"
- "build an animation of <topic>"

If the request looks decorative (hero animations, scroll parallax, page-load reveals), defer to the `frontend-design` skill instead.

## How discovery works (the meta-principle)

**Every visual decision is a guided choice, never an imposition.** The agent presents 2-4 explicit options for each decision, names one as recommended (with a one-sentence reason), and offers an opt-in browser preview whenever the choice is visually distinguishable. The user picks. If the user says *"you decide"*, the agent picks the recommended option and **announces** it ("voy con Voltage por X"); never silent.

This applies to every step below: topic, pattern, palette, typography, complexity, output mode, layout variant, interactivity, export resolution/fps/aspect. If you find yourself making a visual decision the user did not pick, stop and ask — even if the choice feels obviously right.

The only thing the skill *imposes* (non-negotiable) is the hard rules in [§ The 3 hard rules](#the-3-hard-rules): motion = pedagogy, one focal point, always replayable.

## 5-step discovery protocol (always start here)

Before writing code, ask the user. Default to "you choose" if they say so — pick the highest-ranking match and explain why in one sentence.

**1 — Topic.** "What do you want to animate?" Skip if the request already has enough detail.

**2 — Pattern.** Show 3-4 patterns from the catalog the topic fits, with one-line previews. See [`patterns/_index.md`](./patterns/_index.md). Recommend one based on the topic.

> **Optional visual preview.** Before locking the pattern, ask: *"Want to see a 10-second example of each in your browser before deciding?"* — if yes, open the matching reference HTMLs via the OS default opener (`open` on macOS, `xdg-open` on Linux). The skill ships with examples for patterns A, B, M, N, O, P (see [`previews/_index.md`](./previews/_index.md)). For patterns without a pre-built example, skip the offer and describe in words. If the user says no, continue without the preview.

**3 — Visual style.**
- **Palette**: propose 3 alternatives — Voltage (default), Editorial, Neon dark. Full options in [`library/colors.md`](./library/colors.md). **Optional preview**: ask *"Want to see each palette side-by-side in your browser?"* — if yes, open the 3 HTML swatches at [`previews/palettes/`](./previews/palettes/) one by one (or all 3 at once).
- **Typography**: propose 3 pairings — Geist+Geist Mono (default), Fraunces+JetBrains Mono, Space Grotesk+IBM Plex Mono. See [`library/typography.md`](./library/typography.md). **Optional preview**: open the 3 HTML samples at [`previews/typography/`](./previews/typography/).
- **Icons/images**: ask whether the user (a) provides assets, (b) wants Claude to find them, or (c) accepts AI-drawn SVG. See [`library/icons.md`](./library/icons.md).

**4 — Complexity.** "How many steps / components? (4-6 digestible, 8-12 thorough, 15+ chapter it)."

**5 — Output mode + interactivity + export.**

> **5a — Output mode (ask this FIRST in step 5, before anything else).** The two modes are **mutually exclusive within a single widget** — pick ONE; if the user needs both, that's two widgets generated in sequence, not a hybrid option.
>
> - **Browser-native** — the user opens the HTML, reads + interacts. The layout is a **vertical scroll** with full-width step cards, infinite height, free aspect ratio. Optimised for reading. **NOT suitable for video export** (recording produces a long thin file with scroll, unusable for social/landscape).
> - **Video-target** — the layout fits a **single fixed frame** (16:9 / 9:16 / 1:1) with no scroll. Animation reveals content *inside* the frame: cursor descends, layers expand/collapse in place, cards appear and disappear; the camera does not move. The Export button + agent-side renderer produce a usable WebM/MP4.
>
> **Present exactly two options. Do not offer "both" / "either" / "let me decide later" / "do both separately" as a single choice** — these create ambiguous geometry and the widget ends up serving neither use well. If the user truly needs both, ask which they want NOW; after delivering that widget, offer to generate the other variant as a separate file.
>
> **Optional visual preview.** Before locking the mode, ask: *"Want to see a live example of each in your browser? They look very different."* — if yes, open the three HTML demos (browser-native + video 16:9 + video 9:16) via the OS opener (`open` on macOS, `xdg-open` on Linux):
> - `previews/output-modes/browser-native.html`
> - `previews/output-modes/video-target-16-9.html`
> - `previews/output-modes/video-target-9-16.html`
>
> Each demo is a fully animated mini-example of the *same* topic (a transformer pipeline) so the user can directly compare how the geometry differs.
>
> **Defaults (use when the user did not pick explicitly):**
> - Verbs "understand / explain / learn / study / tutorial / docs" → browser-native
> - Verbs "reel / short / video / post / share / social / youtube / tiktok / instagram" → video-target
> - Didactic family (A-L) without social verbs → browser-native
> - Content-creator family (M-P) → video-target
>
> Full layout rules in [`library/output-modes.md`](./library/output-modes.md).

**5b — Layout variant (sub-shape within the chosen output mode).** Once mode + aspect are decided, **the geometry still has many valid shapes** depending on the pattern. Present 2-3 layout variants with a recommendation:

| Pattern family | Layout variants offered in video-target |
|---|---|
| **Flow / pipeline** (A, B, I, K) | `flow` — header + title + focal + token-stream + progress (default); `stack-compact` — all steps visible as mini-cards, current expanded; `cursor-timeline` — vertical timeline with cursor descending |
| **Comparison** (D) | `split-horizontal` — top vs bottom (default for 9:16); `split-vertical` — left vs right (default for 16:9) |
| **Algorithm / cursor** (C) | `data-structure-focus` — full-frame structure + cursor (default); `code-and-vis` — split code left + viz right (16:9 only) |
| **Math reveal** (E) | `formula-centered` — formula grows term-by-term in middle; `derivation-stack` — each step appears below the previous |
| **Mechanical / orbital / particles** (F, G, H) | `fullscreen-system` — system fills the frame; `system-plus-caption` — system + step caption at bottom |
| **Timeline / sequence** (L) | `horizontal-axis` — left-to-right (default for 16:9); `vertical-axis` — top-to-bottom (default for 9:16) |
| **Geo / map** (J) | `full-map` — map fills frame; `map-plus-overlay` — map + step caption + data badge |
| **Text effects** (M) | `text-fullscreen` — text fills frame; `text-with-tag` — text + small tag below |
| **Counter / clock** (N) | `big-number-centered` — number is 60-70% of frame height; `counter-plus-context` — number + label below |
| **Shape morph** (O) | `shape-fullscreen` — single morphing shape; `shape-grid` — 4 shapes in 2×2 grid morphing in sync |
| **Line drawing** (P) | `line-fullscreen` — single trace; `line-plus-label` — trace + caption |

Recommend the *default* listed above for the chosen pattern, but let the user pick. If they pick something unusual, ask why (might lead to a better recommendation).

**5c — Base controls.** Confirm Play/Pause/Restart/Speed are always included.

**5d — Extras.** Path selector, step-through mode, annotations.

**5e — Export.** Only if video-target was chosen in 5a, ask resolution/fps/aspect ratio — see [`library/export.md`](./library/export.md). For browser-only, skip export questions (the in-widget Export button still works, but warn the user the output won't be a clean video without rebuilding in video-target mode).

### Closing the discovery — keep it user-oriented

When the 5 steps are done, summarize the decisions in **the user's language** in 2-3 short sentences, framed by *what they're about to see* — never by what docs / libraries / cheatsheets you're about to read. Internal preparation is invisible to the user.

❌ Bad: "Decisiones tomadas. Voy a leer la doc del patrón I, las librerías de estilo y el cheatsheet de Anime.js v4 antes de escribir el widget."

✅ Good: "Listo. Voy a armarte una animación del flujo del transformer paso a paso — input → tokens → embeddings → atención → salida — en paleta Voltage, tipografía Geist. Te paso el preview en el navegador en un momento."

Format: (a) what they'll see, (b) which style, (c) when/how they get it.

## The 3 hard rules

1. **Motion = pedagogy.** Every animated frame teaches the next idea. If removing motion doesn't hurt the explanation, remove it.
2. **One focal point at a time.** Use dim + highlight aggressively.
3. **Always replayable + controllable.** Play / Pause / Restart + speed are not optional.

If any rule is broken, redo it.

## Pattern catalog

Sixteen patterns in two families. Each has its own doc under [`patterns/`](./patterns/). Pick by what's being explained or by the creator effect needed.

### Family 1 — Didactic (teach a concept)

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

### Family 2 — Content-creator (capture attention)

| Code | Pattern | Use for |
|---|---|---|
| **M** | [Text effects](./patterns/M-text-effects.md) | Scramble, split, stagger, magnet, wave, type-on, mask reveal |
| **N** | [Numeric counter / clock](./patterns/N-counter.md) | Big number reveals, star counters, ticking clocks |
| **O** | [Shape morph / layered transforms](./patterns/O-shape-morph.md) | Abstract geometry loops, polygon mutation, generative bg |
| **P** | [SVG line drawing](./patterns/P-svg-line-drawing.md) | Sound waves, sonar, route reveals, signatures, sine traces |

Tie-breaker for didactic: L → A → B → I → K → F → G → H → J → C → D → E.
For creator content the user picks the effect directly — there's rarely a "wrong" choice among M/N/O/P.

## Shared style references

- [`library/output-modes.md`](./library/output-modes.md) — browser-native vs video-target layout rules (decided in step 5a)
- [`library/colors.md`](./library/colors.md) — 3 palette presets + semantic tones + path colors
- [`library/typography.md`](./library/typography.md) — 3 typography pairings + role mapping
- [`library/icons.md`](./library/icons.md) — emoji vs Lucide vs custom SVG vs user-provided
- [`library/controls.md`](./library/controls.md) — controls strip spec (Play/Pause/Restart/Speed/Path/Status)
- [`library/timing.md`](./library/timing.md) — duration/delay/easing reference table
- [`library/export.md`](./library/export.md) — export-to-video pipeline (bundled `scripts/export-widget.py` + manual recording + CCapture + Puppeteer + Remotion roadmap)

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

## Companion skills in this plugin

This `animate` skill is the full-flow entrypoint (discovery → pick pattern → build widget → deliver URL or MP4). The plugin also exposes **focused sub-skills** for cases where the user wants only part of the flow:

| Sub-skill | When the agent invokes it |
|---|---|
| `/explanatory-animations:pick-pattern` | User has a topic but doesn't know which of the 16 patterns fits. Outputs a recommendation, no widget. |
| `/explanatory-animations:build-widget` | User already chose a pattern + has content. Outputs an HTML file, no export. |
| `/explanatory-animations:export-widget` | User has a widget HTML and wants a preview URL or MP4 file. Runs `scripts/render.py`. |
| `/explanatory-animations:add-export-button` | User has a widget HTML and wants a click-to-export button inside the page (browser-only, no server). |

When in doubt, `animate` runs the whole pipeline. The focused sub-skills are for when the user has explicitly skipped a step (e.g. "I already have the widget, just give me an MP4" → `export-widget`).

All sub-skills read the shared assets in this skill's directory: `patterns/`, `library/`, `engine/`, `widget-helpers/`, `scripts/`. They reach them via `../animate/<asset>` from their own folder.

## How to build a widget

Each pattern doc (`patterns/X-name.md`) contains:
- A complete **Anime.js skeleton** section with copy-paste starting code
- The required input shape (data the user must provide)
- Variants and pitfalls specific to that pattern

Combine with the shared style libraries (`library/colors.md`, `typography.md`, `controls.md`, `timing.md`) to generate a complete self-contained HTML widget — no build step, just one `.html` file with inlined CSS + JS + Anime.js v4 from `esm.sh`.

The `examples/` folder is **optional reference material** for humans who want to preview "what does Pattern N feel like." Pattern docs are self-contained — building a new animation does not require opening an example file.

## Delivery — two complementary paths

### Path 1 — In-widget Export button (the user clicks, browser does it all)

**Drop `widget-helpers/export-button.js` into ANY widget the skill generates** and a floating "⬇ Export" button appears in the bottom-right. The user clicks it, picks aspect / resolution / fps / duration, and the browser records the timeline frame-by-frame, downloading a WebM file. No server, no Playwright, no Remotion port required.

```html
<!-- One line at the bottom of any widget HTML the skill generates: -->
<script src="${CLAUDE_SKILL_DIR}/widget-helpers/export-button.js" defer></script>
```

Works because all skill-generated widgets respect the `window.timeline` convention (see `library/controls.md`). The button rasterizes via `html2canvas` per frame and assembles WebM via `CCapture.js` — both lazy-loaded from CDN on first click.

Convert to MP4 if the user needs `.mp4` strictly: skill's `scripts/render.py` accepts a `.webm` file and runs it through bundled ffmpeg. Or the user runs `ffmpeg -i animation.webm -c:v libx264 reel.mp4`.

### Path 2 — Agent-side autonomous render (no UI, just deliver)

When the user wants the animation delivered as a URL to preview or as an MP4 file, **the agent invokes `scripts/render.py` directly via Bash** — the user does not install or configure anything. On first run the script bootstraps a private venv under `~/.cache/explanatory-animations/venv` with Playwright + Chromium + a bundled ffmpeg (`imageio-ffmpeg`). Subsequent runs reuse the cache (cold start < 200ms).

```bash
# 1. Agent writes the widget HTML to a temp path it controls:
WIDGET="$(mktemp -d)/widget.html"
cat > "$WIDGET" <<'EOF'
   <!-- the agent generates the widget from patterns/X-name.md skeleton + style libs -->
EOF

# 2a. Preview URL — agent prints the URL for the user to open
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py --widget "$WIDGET"
#   → emits a JSON line: {"mode":"preview","url":"http://localhost:54321/widget.html",...}
#   → opens a browser tab automatically
#   → server runs until Ctrl+C OR --timeout seconds

# 2b. MP4 file — agent prints the resulting file path for the user
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py \
    --widget "$WIDGET" \
    --out "$(dirname "$WIDGET")/reel.mp4" \
    --resolution 1080x1920 \
    --fps 60 \
    --duration 6
#   → emits a JSON line: {"mode":"video","out":"...reel.mp4","size_kb":8345,...}
```

**Bootstrap details (agent does not narrate these to the user — they happen silently):**

| First-time install | Subsequent runs |
|---|---|
| Creates `~/.cache/explanatory-animations/venv` | Reuses existing venv |
| `pip install playwright imageio-ffmpeg` (~50 MB) | No-op (stamp file check) |
| `playwright install chromium` (~140 MB) | No-op |
| Writes stamp file (deps version) | Skips when stamp matches |

The agent's responsibility is just to:

1. Confirm the discovery protocol (topic / pattern / style / complexity / export).
2. Write the widget HTML to a temp path.
3. Invoke `scripts/render.py` with `--out path.mp4` (deliver MP4) or no `--out` (deliver preview URL).
4. Hand the JSON-line output to the user as either "Open this URL: …" or "Your MP4 is at: …".

Never tell the user to install Playwright / ffmpeg / Node / npm — the script handles all of that automatically. If the bootstrap fails (e.g. offline / network blocked / disk full) the script prints a clear error and the agent surfaces it to the user.

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
