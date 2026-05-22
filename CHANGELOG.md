# Changelog

All notable changes to **explanatory-animations** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

### Added
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

[Unreleased]: https://github.com/NightZpy/explanatory-animations-skill/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.4.0
[0.3.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.3.0
[0.2.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/NightZpy/explanatory-animations-skill/releases/tag/v0.1.0
