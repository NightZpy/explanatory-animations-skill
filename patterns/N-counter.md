# Pattern N — Numeric counter / clock

## Use when

- Big number reveal: "50,000 stars", "$1M raised", "10,000 users"
- Live counter for social posts (CTA "click to ⭐")
- Clock / time display with smooth digit rolling (Pattern from "Clock playback controls" demo)
- KPI dashboards animating in
- Score / point counters in gameplay clips
- "We've shipped X commits" project stats

## Don't use when

- The number is part of body copy — keep static
- The number changes faster than ~5 Hz — readers can't track that, use a progress bar instead

## Inputs the user must provide

```js
{
  from:  0,
  to:    50000,
  duration: 4000,
  format: "comma" | "currency-usd" | "k-suffix" | "time-hhmmss" | "custom",
  ease: "outExpo" | "cubicBezier(1,0,1,1)" | "linear",
  decimals: 0,                      // round to N decimals
  prefix: "$",
  suffix: " users",
  trigger: "auto" | "scroll" | "click",   // when to start
}
```

## N.1 — Simple value animate (the workhorse)

```js
import { animate, utils } from "https://esm.sh/animejs@4";

animate('.count', {
  innerHTML: [0, 50000],
  modifier: utils.round(0),
  duration: 4000,
  ease: 'cubicBezier(1,0,1,1)',       // exponential ramp — slow → fast → snap
});
```

The `modifier` is essential — without it the counter shows `0`, `0.001`, `0.002`, ... Wrap with the format function below for thousands separators.

```js
modifier: (v) => Math.round(v).toLocaleString();   // "50,000"
modifier: (v) => '$' + Math.round(v).toLocaleString();   // "$50,000"
modifier: (v) => (v / 1000).toFixed(1) + 'k';      // "50.0k"
```

## N.2 — Multi-stage counter (the "star button" reel)

The "50K stars" Anime.js demo: starts slow, accelerates wildly, settles at the final value. Driven by a multi-segment value animation:

```js
createTimeline()
  .add('.count', {
    innerHTML: ['5', '40000'],            // fast ramp up
    modifier: utils.round(0),
    ease: 'cubicBezier(1,0,1,1)',
    duration: 5000,
  })
  .add('.count', {
    innerHTML: '49999',                   // slow approach to final
    modifier: utils.round(0),
    ease: 'cubicBezier(0,1,0,1)',
    duration: 4250,
  }, '<')                                  // overlap with previous
  .set('.count', { innerHTML: '50000' });  // snap to clean final number
```

The two bezier curves (`(1,0,1,1)` and `(0,1,0,1)`) give the characteristic "speed up then ease out" sensation. Iconic to the Anime.js homepage demo.

## N.3 — Clock with flip-digit cards (3D rotation)

Each digit lives in a `.slot` that's a 3D transform-style container. Inside, ten child `<div>`s (one per digit 0-9) are arranged in a vertical cylinder via `rotateX`.

```js
// Build the cylinder
const $slot = document.querySelector('.slot');
for (let i = 0; i < 10; i++) {
  const $num = document.createElement('div');
  $num.textContent = i;
  utils.set($num, { rotateX: i * 36, z: '3ch' });   // 36° per digit (360°/10)
  $slot.appendChild($num);
}

// Animate the rotation of the slot itself to "scroll" through digits
animate($slot, {
  rotateX: -360,                       // one full revolution per period
  duration: 1000,                       // 1s per digit at 1× speed
  loop: true,
  ease: 'linear',
});
```

Combine multiple slots (hours / minutes / seconds) for a clock. The "Clock playback controls" demo binds a master timeline's `currentTime` to actual time-of-day for live updates.

## N.4 — KPI reveal (sequenced cards)

For "we shipped X / Y / Z" stats:

```js
createTimeline()
  .add('.kpi-1 .count', { innerHTML: [0, 1234], modifier: utils.round(0), duration: 1200 })
  .add('.kpi-2 .count', { innerHTML: [0,   42], modifier: utils.round(0), duration: 1200 }, '-=600')
  .add('.kpi-3 .count', { innerHTML: [0, 9999], modifier: utils.round(0), duration: 1200 }, '-=600');
```

Stagger via `-=` overlaps so each KPI starts before the previous finishes — feels energetic without being chaotic.

## N.5 — Scroll-triggered (count when in view)

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      animate(e.target.querySelector('.count'), {
        innerHTML: [0, parseInt(e.target.dataset.to)],
        modifier: utils.round(0),
        duration: 2000,
      });
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-to]').forEach(el => observer.observe(el));
```

Best for landing pages — counts fire as the section scrolls into view.

## N.6 — Particle burst on increment (the "star burst")

Combine N.1 with a particle spawn at each increment:

```js
function increaseCount() {
  // Spawn a star particle that flies up + fades
  const $star = $starTemplate.cloneNode(true);
  $animation.appendChild($star);
  animate($star, {
    translateY: { to: utils.random(-175, -225), ease: 'out' },
    translateX: [{ from: 0, to: utils.random(-40, 40) }, { to: utils.random(-40, 40) }],
    color: { from: '#FFDD8E' },
    scale: [1, 1.2, 1, .8],
    ease: 'inOut(2)',
    opacity: [1, 0],
    duration: 1000,
    complete: () => $star.remove(),
  });
}
```

Trigger on each click, or in a `setInterval` at counter-update rate.

## Variants

- **Time of day** (Pattern N.3) — clock that ticks live, can be sped up / reversed for time-machine reels.
- **Reverse counter** (N → 0) — for countdowns / "X spots left".
- **Currency with cents** — `modifier: (v) => '$' + v.toFixed(2)`.
- **K / M / B suffixes** — auto-format for >1000, >1M, etc.
- **Multi-line** — "1,234 / 50,000 funded" (two counters, one ratio).

## Pitfalls specific to N

1. **No `modifier`** — counter shows decimals (`50000.0001`) instead of clean integers.
2. **`ease: 'linear'`** for the big reveal — feels mechanical. Use `cubicBezier(1,0,1,1)` for exponential-feel.
3. **Counter starts before the reader sees it** — use scroll trigger or auto-detect visibility.
4. **No font-variant-numeric: tabular-nums** — digits jiggle as they change width. Always set on the counter element.
5. **Multi-digit clock with linear interpolation between digits** — looks janky. Use per-digit rotation as in N.3.
6. **No commas in big numbers** — `50000` is unreadable. Use `toLocaleString()` or a thousands-separator helper.

## Recommended CSS

```css
.count {
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum';
  display: inline-block;
  min-width: 4ch;
  text-align: right;
}
```

`tabular-nums` ensures all digits have the same width — counter doesn't jump as numbers change length.
