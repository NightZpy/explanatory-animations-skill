# Changelog

All notable changes to **explanatory-animations** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

## [0.5.0] — 2026-05-22

### Changed
- **Discovery is now explicitly option-based, never imposing.** SKILL.md gained a new top-level section *"How discovery works (the meta-principle)"* that codifies the rule: every visual decision is presented as 2-4 options with a one-sentence recommendation; the user picks; if the user says *"you decide"* the agent picks the recommendation AND announces it (never silent). The only thing the skill imposes is the 3 hard rules (motion = pedagogy / one focal point / always replayable).
- **New discovery step 5b — Layout variant**, between output mode and base controls. Once mode + aspect are decided, the geometry within still has many valid shapes per pattern (flow / stack-compact / cursor-timeline for flows; split-horizontal vs split-vertical for comparisons; text-fullscreen vs text-with-tag for text effects; big-number-centered vs counter-plus-context for counters; etc.). SKILL.md ships a table of variants per pattern family, with a default per (pattern × aspect ratio).
- **Second 9:16 preview** added (`previews/output-modes/video-target-9-16-counter.html`) — same 1080×1920 stage but in the *big-number* variant (radial accent + 480px counter that ticks 0→2380 with burst particles + bottom context rows) to demonstrate that the same output mode admits very different layouts. The original 9:16 preview is now explicitly labelled as the *flow* variant.
- **Discovery step 5 now asks for output mode FIRST** — *"browser-only or do you also want a video file?"* — before any other interactivity/export question. Picking wrong here is the most expensive mistake (you cannot retrofit a vertical-scroll widget into a single-frame video without regenerating). New doc [`library/output-modes.md`](plugin/skills/animate/library/output-modes.md) defines the two modes (browser-native = scrollable, free aspect; video-target = fixed frame, no scroll, focal-vs-overview split) with explicit layout rules and an auto-default heuristic for the agent.
- **Output mode question now explicitly forbids hybrid options.** The previous wording let the agent offer "both" / "the two things — separate?" as a third choice, which produces a widget that serves neither use well. SKILL.md now says: present exactly two mutually-exclusive options; if the user needs both shapes, generate two widgets in sequence — never one ambiguous hybrid.
- **Output mode gained opt-in visual previews**, alongside the existing previews for palette and typography. Three new self-contained HTMLs under [`previews/output-modes/`](plugin/skills/animate/previews/output-modes/): `browser-native.html` (animated vertical card stack with active-step highlight), `video-target-16-9.html` (1920×1080 stage with overview sidebar + focal area swapping content in place), `video-target-9-16.html` (1080×1920 reel-style with top step-counter, central focal area, progress bar). All three animate the *same* transformer-pipeline topic so the user can directly compare how the geometry differs.
- **Pattern I (Layered transformation)** gained explicit "Output mode" guidance — vertical stack of full-width cards for browser-native vs fixed stage with 25/75 overview-vs-focal split for video-target. Five new pitfalls added.

### Added
- **Anime.js v4 pitfalls section** in `engine/anime-cheatsheet.md` documenting four silent-failure patterns that the previous version omitted: delay-only `.add()` (does nothing in v4), CSS `transform` pre-set conflicting with `animate()`, shared classes with initial `opacity:0` not covered by the timeline's animated-targets selector, restart that rebuilds the DOM instead of `pause + seek(0) + utils.set`.
- **Five new entries in `patterns/_mistakes.md`** (now 15, was 10) covering the same v4 issues from the agent-author perspective. Each entry has bad/good code so the next generation cannot accidentally repeat them.

### Fixed
- **Export button broke at "Start recording"** with `failed to load https://cdnjs.cloudflare.com/ajax/libs/ccapture.js/1.0.9/CCapture.all.min.js` — CCapture.js is **not hosted on cdnjs** at any version. Switched the lazy-load URLs in `widget-helpers/export-button.js` to jsDelivr (primary, `cdn.jsdelivr.net/npm/ccapture.js@1.1.0`) with unpkg as automatic fallback. Also added a fallback chain for `html2canvas` (cdnjs → jsDelivr → unpkg) in case any single CDN is blocked. Updated `library/export.md` and `add-export-button/SKILL.md` to describe the actual sources.

### Added
- **Opt-in visual previews** during the 5-step discovery. When the agent asks the user to pick a pattern, a palette, or a typography pairing, it can now offer *"want to see it in your browser first?"* — if yes, the corresponding self-contained HTML opens via the OS opener (`open` / `xdg-open`, plain `file://`, no server, no deps). Files live under `plugin/skills/animate/previews/`:
  - `previews/palettes/voltage.html`, `editorial.html`, `neon-dark.html` (3/3 palettes)
  - `previews/typography/geist.html`, `fraunces.html`, `space-grotesk.html` (3/3 pairings)
  - Pattern previews reuse the existing `examples/*.html` (6/16 available — A, B, M, N, O, P; the rest fall back to text-only description for now)
  - Index + convention documented in `previews/_index.md`.
- **User-oriented closing message** for the discovery — the SKILL.md now explicitly tells the agent not to narrate "I'll read pattern doc X and library Y before writing the widget"; instead, summarize *what the user will see, in which style, and when*. Bad/good examples included in the SKILL.md.
- GitHub Actions workflow (`.github/workflows/validate.yml`) — runs on every push + PR, validates the plugin manifest, the SKILL.md structure of every sub-skill, and pattern doc completeness.
- `CHANGELOG.md` (this file).
- `CONTRIBUTING.md` with pattern-author guidelines + PR conventions.
- Issue + PR templates under `.github/`.
- `docs/` directory for screenshots, GIFs, and demo videos referenced by the README (assets will be added later by the maintainer).
- README rewritten as a marketplace-ready landing page with feature catalog, quick-start, export pipeline overview, FAQ, and roadmap.

### Changed
- `plugin.json` keywords expanded for discoverability.
- README now treats the plugin as the primary install path; standalone-skill mode documented as legacy.

## [0.4.0] — 2026-05-21

### Added
- **Preflight `doctor.py`** that reports what's installed, what's missing, what would be downloaded — without installing anything. Emits JSON for agents + human summary for users. Three statuses: `READY` / `NEEDS_BOOTSTRAP` / `BLOCKED`.
- **Consent prompt** in `render.py` before downloading ~175 MB on first run. Honors `--yes` / `--no-bootstrap` / `--doctor`. Auto-yes when stdin isn't a TTY (agent context).
- **System ffmpeg reuse** — `render.py` checks for an existing `ffmpeg` on PATH and skips the `imageio-ffmpeg` install if found, saving ~25 MB.
- **5 namespaced skills** under `skills/`:
  - `animate` — full flow (discovery → build → deliver) + holder of shared `patterns/`, `library/`, `engine/`, `widget-helpers/`, `scripts/`.
  - `pick-pattern` — runs only the pattern-selection step.
  - `build-widget` — pattern + content → HTML widget.
  - `export-widget` — widget HTML → preview URL or MP4 via `render.py`.
  - `add-export-button` — inject the floating in-browser Export button into an existing widget.
- `.claude-plugin/plugin.json` manifest enabling `/plugin install` distribution + marketplace submission.

### Changed
- Repo restructured from standalone skill (`SKILL.md` at root) to plugin layout (`skills/<name>/SKILL.md` + manifest). The `main` branch now ships the plugin.
- `render.py` DEPS_VERSION bumped to `v2` (invalidates v1 caches due to system-ffmpeg reuse change).

## [0.3.0] — 2026-05-20

### Added
- Six standalone HTML reference implementations (Anime.js v4) under `examples/`:
  - `lifecycle.html` (Pattern A — state machine)
  - `system-flow.html` (Pattern B — ByteByteGo-style architecture with orthogonal arrows + numbered badges + glowing packet)
  - `text-scramble.html` (Pattern M — 4 effect variants: scramble / cascade / wave / magnet)
  - `counter-stars.html` (Pattern N — 50K star counter with particle burst)
  - `shape-drift.html` (Pattern O — layered SVG with randomized keyframes)
  - `sound-wave.html` (Pattern P — 80 lines + 40 concentric circles drawing themselves)
- `library/content-creator-uses.md` — reel / shorts / podcast priorities (aspect ratios, hook-in-3-seconds, hidden controls during recording, common creator mistakes).
- `scripts/export-widget.py` — Playwright + ffmpeg one-shot script (later subsumed by `render.py` in v0.4).
- `scripts/export-remotion/` — React + Remotion Studio scaffold with two compositions ported (`Lifecycle`, `TextScramble`) including 1080×1080 + 1080×1920 (9:16) variants.

### Changed
- `lifecycle.html` migrated from Anime.js v3 syntax to v4.
- README updated with the 4 content-creator patterns and the Remotion path.

## [0.2.0] — 2026-05-20

### Added
- **4 content-creator patterns** (Family 2) on top of the original 12 didactic patterns:
  - **M — Text effects** (scramble / split-stagger / type-on / magnet / wave / cascade / mask reveal)
  - **N — Numeric counter / clock** (big-number reveals, star counter, flip-digit clock)
  - **O — Shape morph / layered transforms** (drift, polygon morph, pulse, rotate cascade, path morph)
  - **P — SVG line drawing** (draw-on, trace, sound waves, sonar, sine traces, logo reveal)
- `widget-helpers/export-button.js` — drop-in floating "⬇ Export" button that records ANY widget to WebM directly from the browser via `CCapture.js` + `html2canvas`. No server, no Playwright, no agent needed. Works with all 16 patterns because it depends only on the `window.timeline` convention.
- `library/export.md` restructured around 6 strategies with a chooser table.

### Changed
- **Engine migrated from Anime.js v3 → v4** (incompatible API). All pattern skeletons updated:
  - `anime({...})` → `animate(targets, params)`
  - `anime.timeline()` → `createTimeline()`
  - `easing` → `ease` (and prefix dropped: `easeInOutSine` → `inOutSine`)
  - Named ESM imports only (no global `anime` object)
  - New features used: `text.split()`, `svg.createDrawable()`, `utils.*`, `eases.*`, `createSpring()`, parametric easings `inOut(N)` / `out(N)` / `in(N)`
- `engine/anime-cheatsheet.md` rewritten for v4 with a v3 → v4 migration table.
- Pattern index now maps each of the 24 official Anime.js example folders to the patterns in this skill so users can study real reference code.

## [0.1.0] — 2026-05-20

### Added
- Initial release of the skill (standalone mode, `SKILL.md` at root).
- **12 didactic patterns** (Family 1):
  - A — Lifecycle / state machine
  - B — System flow (ByteByteGo style)
  - C — Cursor over data structure (algorithms)
  - D — Side-by-side comparison
  - E — Term-by-term math reveal
  - F — Mechanical / kinematic
  - G — Orbital / celestial
  - H — Particle flow
  - I — Layered transformation (LLM internals, neural nets)
  - J — Geographic map
  - K — Cross-section / stack
  - L — Timeline / sequence
- **5-step discovery protocol** (topic / pattern / style / complexity / interactivity).
- **Style libraries**: `colors.md` (4 palette presets), `typography.md` (3 pairings), `icons.md` (emoji vs Lucide vs custom SVG vs user-provided), `controls.md` (Play / Pause / Restart / Speed / Path / Status strip), `timing.md` (duration + easing reference), `export.md` (export pipelines).
- **Engine cheatsheet** for Anime.js (initially v3, migrated to v4 in v0.2).
- **One reference implementation** (`examples/lifecycle.html`).
- **MIT license** + README + install instructions.

[Unreleased]: https://github.com/NightZpy/explanatory-animations-skill/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.5.0
[0.4.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.4.0
[0.3.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.3.0
[0.2.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.1.0
