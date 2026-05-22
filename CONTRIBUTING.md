# Contributing to explanatory-animations

Thanks for your interest in extending the skill. This document covers the conventions specific to this plugin so new patterns / examples / fixes land in a consistent way.

## Quick start

```bash
git clone https://github.com/NightZpy/explanatory-animations-skill.git
cd explanatory-animations-skill
# Open with Claude Code in plugin-dir mode for live testing
claude --plugin-dir .
```

Any change to `skills/**/SKILL.md` or supporting files is picked up live by Claude Code via the `--plugin-dir` flag; no restart needed for most edits.

## Adding a new animation pattern

The skill currently exposes 16 patterns (A–P) split into two families: didactic (A–L) and content-creator (M–P). To add a new one, e.g. **Q — Network graph**:

1. **Add a pattern doc** at `skills/animate/patterns/Q-network-graph.md`. Follow the same eight-section structure used by existing pattern docs:
   - `## Use when`
   - `## Don't use when`
   - `## Inputs the user must provide`
   - `## Visual structure`
   - `## Animation choreography`
   - `## Anime.js skeleton` *(copy-paste starting code)*
   - `## Variants`
   - `## Pitfalls specific to <code>`
2. **Add a row** to `skills/animate/patterns/_index.md` under the right family.
3. **Add a row** to the pattern catalog in `skills/animate/SKILL.md`.
4. **(Recommended)** Add a reference implementation at `skills/animate/examples/<code>-<name>.html` using Anime.js v4 + the conventions in `library/controls.md`.
5. **Bump `version`** in `.claude-plugin/plugin.json` (PATCH for additive changes, MINOR if it changes existing patterns, MAJOR if breaking).
6. **Add a `CHANGELOG.md` entry** under `## [Unreleased]`.
7. **Open a PR** with a 1-paragraph rationale: when to use the new pattern vs the existing ones.

The validation workflow checks that every pattern doc has the required sections; PRs missing them fail CI.

## Adding a new style preset

Style presets live in `skills/animate/library/`. The three current palette presets (Voltage / Editorial / Neon dark) are in `colors.md`. To add a fourth:

1. Add the preset block to `colors.md` with token definitions (paper / ink / accent + semantic tones).
2. Mention it in the discovery protocol section of `skills/animate/SKILL.md` (Step 3).
3. Update `skills/pick-pattern/SKILL.md` and `skills/build-widget/SKILL.md` if the new preset is recommended by default for specific topics.

## Adding a new export strategy

There are six strategies documented in `skills/animate/library/export.md` (0 — in-widget button, 1 — autonomous Python script, 2 — manual screen recording, 3 — raw CCapture, 4 — Puppeteer, 5 — Remotion). Adding a seventh means:

1. Add the strategy section to `export.md` with: setup, usage, when to use, pitfalls.
2. Update the chooser table at the top of `export.md`.
3. Consider whether `skills/export-widget/SKILL.md` should know about the new strategy.

## Conventions every contribution must follow

### Widget conventions

Every widget the skill emits must:
- Expose its master timeline as `window.timeline` (so `render.py` and `widget-helpers/export-button.js` can drive it deterministically).
- Honor `?clean=1` URL param to hide its controls strip during recording.
- Wait for `document.fonts.ready` before any layout-sensitive work.
- Respect `@media (prefers-reduced-motion: reduce)` for accessibility.
- Be self-contained — no external CSS file references besides Google Fonts + `esm.sh/animejs@4.x`.

### Anime.js v4 only

The engine reference at `skills/animate/engine/anime-cheatsheet.md` documents v4. Any code that introduces v3 idioms (`anime({...})`, `anime.timeline()`, `easing: "easeInOutSine"`) will be rejected. See the cheatsheet's v3→v4 migration table for the diff.

### Code comments and commits in English

Mirror the convention used in the rest of the project. Code comments + commit messages in English; user-facing text (in pattern descriptions, library docs) can be bilingual EN/ES if useful.

### Versioning

The plugin uses [SemVer](https://semver.org/). When you bump `version` in `plugin.json`, also add a CHANGELOG entry under the new version.

## Running tests

```bash
# CI validation (same checks the GitHub workflow runs)
python3 .github/workflows/validate.yml  # not directly executable — read the YAML and copy commands

# Doctor (preflight check for render.py)
python3 skills/animate/scripts/doctor.py

# Smoke render (writes test.mp4 from an example widget)
python3 skills/animate/scripts/render.py \
    --widget skills/animate/examples/lifecycle.html \
    --out /tmp/smoke-test.mp4 \
    --resolution 1280x720 \
    --fps 30 \
    --duration 3 \
    --yes
```

## PR checklist

- [ ] CHANGELOG.md updated under `## [Unreleased]`
- [ ] If adding / changing a pattern, `patterns/_index.md` + `SKILL.md` catalog updated
- [ ] If adding / changing a strategy, `library/export.md` chooser table updated
- [ ] CI passes (`.github/workflows/validate.yml`)
- [ ] At least one screenshot / GIF if the change is visual

## Reporting bugs

Open a [GitHub issue](https://github.com/NightZpy/explanatory-animations-skill/issues/new/choose) with:
- The pattern / sub-skill involved.
- Browser + OS where the widget was rendered.
- A minimal reproducible widget HTML (when possible).
- Expected vs actual behavior.

## License

By contributing you agree your contribution is released under the MIT license (see [LICENSE](./LICENSE)).
