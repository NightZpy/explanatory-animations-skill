# Timing reference

Defaults that work across patterns. Adjust per pattern (see each pattern doc).

## Per-event durations

| Event | Duration |
|---|---|
| Traveler dot crosses one edge segment (state-machine) | 600–800 ms |
| Packet walks one segment of an orthogonal arrow (system-flow) | 380–480 ms per segment |
| Pause after each arrival (so the highlight is visible) | 200–250 ms |
| Node settle pulse (scale 1 → 1.08 → 1.04) | 320–400 ms |
| Term fade-in (math reveal) | 350 ms |
| Card flip / morph | 450–600 ms |
| Particle spawn-to-sink (particle flow) | 1500–3000 ms (longer feels natural) |
| Orbital revolution (planet) | 3000–10000 ms (one full revolution at 1×) |
| Mechanical cycle (one stroke of a 4-stroke engine) | 1200–2000 ms |
| Traveler fade-out at terminal | 400 ms |

## Total animation length

| Length | When |
|---|---|
| 6–10 s at 1× | Single clear flow — ideal sweet spot |
| 10–15 s at 1× | Complex but still digestible — split into chapters considered |
| 15+ s at 1× | Too long. SPLIT into chapters (separate Play buttons) |

If the user wants a 30-second deep-dive, structure as e.g. "Phase 1: enqueue (8s)", "Phase 2: process (10s)", "Phase 3: persist (6s)". Each chapter has its own play.

## Easings

| Easing | When |
|---|---|
| `easeInOutSine` (default) | Smooth back-and-forth motion, traveler hops, generic |
| `linear` | Constant velocity — packet along a wire, planet at uniform speed |
| `easeOutQuad` | Settle after arrival — scale pulse, fade-in |
| `easeInQuad` | Accelerate from rest — rare; only for "build-up" moments |
| `spring(1, 80, 12, 0)` | Bouncy arrival — playful patterns only, avoid for technical docs |
| `easeInOutCubic` | A bit more dramatic than sine — use sparingly |

Mechanical motion: piston use `easeInOutSine`, gear use `linear`, mixing them is a pitfall.

## Reduced motion

Honor `prefers-reduced-motion` always:

```css
@media (prefers-reduced-motion: reduce) {
  .state-machine *, .bbg2-stage * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

JS-driven anime.js animations should also check:

```js
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const dur = reduced ? 1 : 700;  // collapse durations
```

The reader still sees the highlights advance — instantly — so the explanation still lands.

## Speed multiplier

Global, set via `window.anime.speed`. The Speed Pill values:
- `0.5×` → `anime.speed = 0.5` (durations effectively doubled)
- `1×`   → `anime.speed = 1`
- `2×`   → `anime.speed = 2` (durations effectively halved)

For mechanical / orbital patterns, optionally add `0.25×` for very slow inspection.

## Auto-play timing

- **In view**: 220–280 ms after layout settles (give the host page time to flow).
- **Behind a tab**: trigger on tab activation + 250 ms delay.
- **Below the fold**: `IntersectionObserver` at 0.5 threshold + 250 ms delay after entering view. Do NOT auto-play immediately on page load if widget is below the fold.

## Pause / resume

`anime.timeline().pause()` preserves the timeline position. `play()` resumes from there. Restart is `pause() + seek(0)` then a fresh `play()` cycle.

## Mistakes to avoid

1. **`anime.speed` set after `anime.timeline()` started** — set it BEFORE creating the timeline so all child instances inherit.
2. **Too fast at 1× for mechanical/orbital** — readers can't track 60 RPM at 1×. Default to 0.5× and let them speed up.
3. **No delay between hops** — flow looks rushed, reader misses arrivals. 200ms minimum.
4. **Easing mismatch** in mechanical (piston `linear`, gear `easeInOutSine` — should be inverted).
5. **Reduced motion ignored** — animation still runs full speed for users who explicitly opted out.
