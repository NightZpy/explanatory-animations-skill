# Examples

Reference implementations for the patterns. Open any `.html` directly in a browser — no build step. All use **Anime.js v4** loaded from `esm.sh`.

## Family 1 — Didactic

| File | Pattern | Shows |
|---|---|---|
| `lifecycle.html` | A — Lifecycle | Job lifecycle with happy / failure / retry paths, traveler dot walking the active path |
| `system-flow.html` | B — System flow | ByteByteGo-style 2D architecture with boundary regions, orthogonal arrows, numbered step badges, glowing packet |

## Family 2 — Content creator

| File | Pattern | Shows |
|---|---|---|
| `text-scramble.html` | M — Text effects | Scramble / cascade / wave / magnet variants on a hero headline, neon dark theme |
| `counter-stars.html` | N — Numeric counter | Star button counter going from 0 → 50K with particle burst (the iconic Anime.js homepage demo) |
| `shape-drift.html` | O — Shape morph | Layered SVG shapes (circles / rects / triangles) with randomized keyframes — generative background loop |
| `sound-wave.html` | P — SVG line drawing | 80 vertical lines + 40 concentric circles drawing themselves with staggered timing — radio / sonar / audio visualizer |

## Open them

```bash
cd ~/Documents/projects/claude/skills/explanatory-animations/examples
open lifecycle.html             # or any other
```

Or via `python3 -m http.server 8000` from the skill root (some browsers block ESM imports on `file://`).

## Want more patterns

Examples for C–L (algorithm / comparison / math / mechanical / orbital / particle / layered / map / cross-section / timeline) are roadmap items. Until those land, study the official Anime.js examples:

```bash
git clone https://github.com/juliangarnier/anime.git
cd anime/examples
```

24 example folders covering nearly every effect this skill defines. The pattern docs (`patterns/X-*.md`) list which official example maps to which pattern.
