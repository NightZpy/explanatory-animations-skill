---
name: build-widget
description: Generate a self-contained interactive HTML widget for a chosen animation pattern. Use when the user has already picked a pattern (or you ran pick-pattern first) and wants the widget code itself — not the discovery dialogue, not the export. Reads the pattern doc, applies style choices, and emits one .html file with inlined CSS + JS + Anime.js v4. Does NOT export to video — that's `export-widget`.
---

This skill takes a **pattern code + content + style choices** and emits a complete HTML widget. It does not run the discovery protocol (use `animate` for that) and does not export to video (use `export-widget`).

## Inputs (must be provided or asked for)

1. **Pattern code** (`A`–`P`). If missing, ask the user OR invoke `pick-pattern` first.
2. **Content** — the actual data the pattern needs. Each pattern's doc lists exactly what (`../animate/patterns/<code>-<name>.md` → "Inputs the user must provide").
3. **Style choices** (use the user's last answers OR sensible defaults):
   - Palette: Voltage (default) / Editorial / Neon dark / brand-aligned — see `../animate/library/colors.md`
   - Typography: Geist+Geist Mono (default) / Fraunces+JetBrains Mono / Space Grotesk+IBM Plex Mono — see `../animate/library/typography.md`
   - Icons: emoji (default) / Lucide / custom SVG / user-provided — see `../animate/library/icons.md`
   - Output dimensions (optional, default 16:9 landscape)

## Process

1. Open `../animate/patterns/<code>-<name>.md` and copy its **Anime.js skeleton** section verbatim as the JS core.
2. Open `../animate/library/colors.md`, `typography.md`, `controls.md`, `timing.md` for the style contracts.
3. Generate ONE `.html` file with:
   - `<head>`: font preconnect + Google Fonts link for the chosen typography
   - `<style>`: inlined CSS using the chosen palette tokens
   - `<body>`: required controls strip (Play / Pause / Restart / Speed / optional Path / Status) + the stage
   - `<script type="module">`: imports from `https://esm.sh/animejs@4.1.4`, builds the pattern, exposes `window.timeline = tl;` (required convention)
4. Always include:
   - `window.timeline = tl;` so `export-widget` and `add-export-button` can drive the timeline
   - `?clean=1` URL param handling that hides the controls strip (so screenshots/recordings come out clean)
   - `@media (prefers-reduced-motion: reduce)` accessibility fallback
   - Mobile fallback ≤720px (per pattern doc's "Mobile fallback" notes)

## Output format

A single `.html` file (the agent decides the path — `/tmp/anim/widget.html` is conventional). Confirm to the user: file path + how to open it. Do not auto-launch a browser — `export-widget` does that when needed.

## When to hand off

- **User wants to see it now** → invoke `export-widget` with no `--out`. That runs `render.py` in preview mode.
- **User wants an MP4** → invoke `export-widget` with `--out reel.mp4`.
- **User wants to click Export from the browser themselves** → invoke `add-export-button` to inject the floating Export button.

## Referenced files

- `../animate/patterns/<code>-<name>.md` — the skeleton + variants + pitfalls for the chosen pattern
- `../animate/library/colors.md` · `typography.md` · `icons.md` · `controls.md` · `timing.md` — style contracts
- `../animate/engine/anime-cheatsheet.md` — Anime.js v4 API reference if the pattern skeleton needs adjusting

## Output checklist (before declaring done)

- [ ] Pattern explicitly chosen from the catalog (A–P)
- [ ] Anime.js skeleton from the pattern doc adapted to the user's content
- [ ] 3 core animation rules respected: motion = pedagogy / one focal point / replayable + controllable
- [ ] `window.timeline = tl;` present
- [ ] Controls strip rendered (or `?clean=1` hides it)
- [ ] `prefers-reduced-motion` honored
- [ ] No diagonal arrows in B / J / K layouts; orthogonal only
- [ ] Edge labels have background rects for legibility (B / J / K)
- [ ] Self-contained — no external CSS file references besides Google Fonts + esm.sh
