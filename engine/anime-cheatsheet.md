# Anime.js v3 cheatsheet

The APIs you'll actually use, ordered by frequency.

## Load

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js" defer></script>
```

Confirm with `if (window.anime) { ... }` before calling.

## Single animation

```js
anime({
  targets: '.box',         // CSS selector, DOM node, or array of either
  translateX: 250,         // any animatable CSS property
  duration: 800,
  delay: 200,
  easing: 'easeInOutSine',
  autoplay: true,
});
```

## Timeline (most common for explanatory animations)

```js
const tl = anime.timeline({
  easing: 'easeInOutSine',
  duration: 700,            // default for all .add() calls without explicit duration
  begin:    () => setStatus('playing', 'playing'),
  complete: () => setStatus('done'),
});

tl.add({ targets: '#node-1', scale: 1.06 })
  .add({ targets: '#packet', cx: 240, cy: 100 })     // chained: starts after previous
  .add({ targets: '#node-2', scale: 1.06 }, '-=200') // overlap previous by 200ms
  .add({ targets: '#packet', opacity: 0 });
```

`.add(params, offset?)` — `offset` is `'-=N'` to overlap or `'+=N'` to delay. Skip for sequential.

## Stagger (multiple targets, offset between each)

```js
anime({
  targets: '.particle',
  translateX: 400,
  delay: anime.stagger(100),       // 0ms, 100ms, 200ms, ...
  // or:
  delay: anime.stagger(100, { start: 500 }),        // start at 500ms then stagger
  // or radial:
  delay: anime.stagger(50, { grid: [10, 10], from: 'center' }),
});
```

## Keyframes (multi-step single target)

```js
anime({
  targets: '#piston',
  keyframes: [
    { translateY: 0,   easing: 'easeInOutSine' },
    { translateY: 100, easing: 'easeInOutSine' },
    { translateY: 0,   easing: 'easeInOutSine' },
  ],
  duration: 1200,
  loop: true,
});
```

## Loops (orbital, mechanical)

```js
anime({
  targets: '#planet-orbit',
  rotate: 360,
  duration: 3650,
  loop: true,
  easing: 'linear',
  autoplay: false,           // start on user gesture
});
```

`loop: true` runs forever. `loop: 3` runs 3 times then stops.

## Direction

```js
direction: 'normal'    // default
direction: 'reverse'   // run backwards
direction: 'alternate' // forward then backward (great for pulses)
```

## Easings (the ones to know)

| Easing | Curve |
|---|---|
| `linear` | constant velocity — use for orbits, gears, particles on a wire |
| `easeInOutSine` | smooth back-and-forth — default for hops |
| `easeOutQuad` | settle into a position — scale pulses, fade-in |
| `easeInQuad` | accelerate from rest — rare, "build-up" moments |
| `easeInOutCubic` | dramatic version of sine — sparingly |
| `spring(1, 80, 12, 0)` | bouncy arrival — playful only |
| `easeInOutBack` | overshoots — never in technical animations |

## Global speed multiplier

```js
window.anime.speed = 0.5;     // half speed
window.anime.speed = 2;       // double speed
```

**Set BEFORE creating the timeline.** Mid-flight changes affect only future animations.

## Motion along an SVG path

```js
const path = anime.path('#my-svg-path');

anime({
  targets: '.dot',
  translateX: path('x'),
  translateY: path('y'),
  rotate:     path('angle'),   // align dot's orientation with the path tangent
  duration: 2000,
  easing: 'linear',
});
```

Use for particle flow (Pattern H), great-circle arcs (Pattern J), curved trajectories.

## Pausing / resuming

```js
const tl = anime.timeline({ ... });
tl.add({ ... });

tl.pause();             // freezes
tl.play();              // resumes from where paused
tl.restart();           // resets to 0 + plays
tl.seek(500);           // jump to t=500ms
tl.reverse();           // toggles direction

console.log(tl.progress);   // 0..100
console.log(tl.paused);     // boolean
```

## Callbacks per animation

```js
anime({
  targets: '#x',
  translateX: 100,
  begin:      anim => console.log('starting'),
  update:     anim => console.log(anim.progress),  // every frame
  complete:   anim => console.log('done'),
  loopBegin:  anim => console.log('new loop'),
  changeBegin: anim => console.log('keyframe boundary'),
  changeComplete: anim => console.log('keyframe boundary'),
});
```

The `update` callback fires every animation frame — perfect for syncing side effects (light up an arrow halfway through a packet's traversal, update a counter, etc).

## SVG line-drawing trick (handy for connectors)

```js
anime({
  targets: '.svg-line',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 800,
});
```

Pre-set `stroke-dasharray` = the path length, then animate `stroke-dashoffset` from `dasharray` → 0 to "draw" the line.

## Animatable CSS properties

Most common: `translateX`, `translateY`, `translateZ`, `scale`, `scaleX`, `scaleY`, `rotate`, `opacity`, `width`, `height`, `borderRadius`, `backgroundColor`, `color`, `fill`, `stroke`, `strokeDashoffset`, `cx`, `cy`, `r` (SVG circles), `x1`, `y1`, `x2`, `y2` (SVG lines), `d` (SVG paths — for morphing).

## Custom properties / CSS variables

```js
anime({
  targets: ':root',
  '--my-var': 100,
  duration: 1000,
});
```

Animate CSS custom properties — useful for cascading visual changes.

## Common gotchas

1. **`scale` resets `transform-origin`** — default is center. To rotate a planet around the sun, set `transform-origin: 400px 300px;` on the orbit `<g>` first.
2. **Animating `width`/`height` is slow** — use `scale` for performance when possible.
3. **`anime({})` without `autoplay: false` starts immediately** — set `autoplay: false` if you want to drive playback manually.
4. **Timeline children inherit `easing` and `duration` from parent** — but per-`add` overrides win.
5. **Multiple `anime()` on same target** — last call wins; older animations are NOT cancelled automatically. Use `anime.remove(target)` to cancel.

## Migrating to Anime.js v4 (later)

Anime.js released a v4 with a different API (`createAnimation`, `createTimeline`, named imports). This skill targets v3 for stability + CDN simplicity. If you migrate, every call signature changes — see <https://animejs.com> for the new docs.

## Resources

- Official docs: <https://animejs.com>
- v3 source: <https://github.com/juliangarnier/anime/tree/v3.2.1>
- Easings playground: <https://animejs.com/documentation/#cssEasings>
