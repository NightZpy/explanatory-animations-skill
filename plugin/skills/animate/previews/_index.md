# Visual previews (opt-in)

Self-contained HTMLs the agent can open in the user's browser via `file://` (no server, no deps) when the user wants to *see* an option before choosing it. Each step of the 5-step discovery offers a preview; the user can decline and the flow continues normally.

How the agent opens them:

```bash
# macOS
open "${CLAUDE_SKILL_DIR}/previews/palettes/voltage.html"
# Linux
xdg-open "${CLAUDE_SKILL_DIR}/previews/palettes/voltage.html"
```

If multiple options should be compared, open them one after another (the user keeps tabs open and switches between them).

## What's available

| Decision | Previews available |
|---|---|
| **Output mode** (step 5a) | Browser-native, Video-target 16:9, Video-target 9:16 (3/3) |
| **Pattern** (step 2) | A, B, M, N, O, P (see `../examples/`) — 10 remaining patterns described in text only |
| **Palette** (step 3) | Voltage, Editorial, Neon dark (3/3) |
| **Typography** (step 3) | Geist+Geist Mono, Fraunces+JetBrains Mono, Space Grotesk+IBM Plex Mono (3/3) |

## Output mode previews

The most impactful preview set — they show how the same topic looks under each geometry, side by side. Always offer these when the user is unsure about output mode.

- `output-modes/browser-native.html` — vertical scrollable card stack with active-step highlight
- `output-modes/video-target-16-9.html` — fixed 1920×1080 stage, overview sidebar (25%) + focal area (75%), content swaps in place
- `output-modes/video-target-9-16.html` — fixed 1080×1920 stage, **flow variant** (header + focal + token-stream + progress) — default for Pattern I / L / B / K
- `output-modes/video-target-9-16-counter.html` — same 1080×1920 stage, **big-number variant** (radial accent + huge counter + bottom context block) — default for Pattern N (counter), pattern for any "single dominant element + context" reel

These two 9:16 demos make a key point clear: **the output mode is geometric (frame fixed, no scroll); the layout WITHIN the frame has many valid variants**. The skill picks a default per pattern but the user can override (see step 5b of the discovery in SKILL.md).

## Pattern previews — file paths

| Code | Pattern | Preview file |
|---|---|---|
| A | Lifecycle / state machine | `../examples/lifecycle.html` |
| B | System flow (ByteByteGo) | `../examples/system-flow.html` |
| M | Text effects | `../examples/text-scramble.html` |
| N | Numeric counter | `../examples/counter-stars.html` |
| O | Shape morph | `../examples/shape-drift.html` |
| P | SVG line drawing | `../examples/sound-wave.html` |
| C / D / E / F / G / H / I / J / K / L | — | not yet, describe in words |

## Palette previews

- `palettes/voltage.html` — default; deep blacks + electric accent + soft grays
- `palettes/editorial.html` — cream paper + ink + warm accent
- `palettes/neon-dark.html` — pitch black + neon green/magenta

## Typography previews

- `typography/geist.html` — Geist (sans) + Geist Mono — default, clean utility
- `typography/fraunces.html` — Fraunces (serif) + JetBrains Mono — editorial, magazine
- `typography/space-grotesk.html` — Space Grotesk + IBM Plex Mono — technical, modern

## Convention for adding new previews

Self-contained HTML, no build, Anime.js v4 loaded via `esm.sh` if needed. Width 100vw / height 100vh, dark or light per style. Aim for 5-15 seconds of looped motion or static swatch — enough for the user to read the vibe.
