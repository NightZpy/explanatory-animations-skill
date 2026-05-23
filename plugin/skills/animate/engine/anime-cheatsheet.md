# Anime.js v4 cheatsheet

This skill targets **Anime.js v4** (`v4.1.x` at time of writing). The API is **incompatible with v3** — see the migration note at the end.

## Load

ESM via CDN (the modern way):

```html
<script type="module">
  import {
    animate,
    createTimeline,
    createSpring,
    stagger,
    text,
    svg,
    utils,
    eases,
  } from "https://esm.sh/animejs@4.1.4";
  // your code here
</script>
```

Or pin a specific version: `"https://esm.sh/animejs@4.1.1"`.

## animate() — single animation

```js
animate('.box', {                    // targets first, params second
  translateX: 250,
  scale: 1.2,
  opacity: [0, 1],                   // [from, to]
  duration: 800,
  delay: 200,
  ease: 'inOutQuad',                 // renamed from v3 'easing'
  autoplay: true,
});
```

`animate(targets, params)` returns an Animation instance with `.play()`, `.pause()`, `.restart()`, `.seek(t)`, `.reverse()`, `.refresh()`.

## createTimeline() — sequenced animations

```js
const tl = createTimeline({
  defaults: { ease: 'inOutSine', duration: 700 },
  loop: true,
  alternate: true,
  loopDelay: 75,
  onComplete: self => console.log('done'),
  onUpdate:   self => console.log(self.currentTime, self.progress),
})
  .add('.node-1', { scale: 1.06 })
  .add('.packet',  { x: 240, y: 100 })       // sequential
  .add('.node-2',  { scale: 1.06 }, '-=200') // overlap previous by 200ms
  .add('.packet',  { opacity: 0 });
```

Offset syntax in `.add(targets, params, offset)`:
- `'+=N'` — start N ms after previous ends
- `'-=N'` — overlap previous by N ms
- `'<'`   — start at the same time as previous
- `'<<'`  — start at the same time as the one before previous
- `'<+=N'` — anchor to previous start + N ms offset
- `'label'` — start at a label position (set via `.label('myLabel', offset)`)

Position-keyed control adds (no targets):
```js
tl.set(target, { props }, position)   // instant set at position
  .call(callback, position)           // fire callback
  .label('name', position)            // mark a position
  .sync(otherTimeline, position)      // nest another timeline
```

## stagger() — offsets across multiple targets

```js
animate('.particle', {
  translateX: 400,
  delay: stagger(100),                              // 0, 100, 200, ...
  delay: stagger(100, { start: 500 }),              // first starts at 500ms
  delay: stagger(100, { from: 'center' }),          // ripple from middle
  delay: stagger(100, { from: 'last' }),            // reverse stagger
  delay: stagger(100, { from: 'random' }),          // randomized
  delay: stagger(50,  { grid: [10, 10], from: 'center' }),  // 2D grid
  delay: stagger([0, 500]),                         // range — first 0, last 500, even spread
  delay: stagger(100, { use: 'data-line' }),        // group by data attribute
});
```

`stagger` returns a function the animation calls per target with `(target, index, total)`.

## Easings

| v4 ease | Description |
|---|---|
| `linear` | Constant velocity. Use for orbits, packet-on-wire. |
| `inOutSine` (default) | Smooth start + finish. Default for hops. |
| `outQuad` / `inQuad` / `inOutQuad` | Quadratic — slightly more dramatic than sine. |
| `outCubic` / `inOutCubic` | Cubic — settle into a position. |
| `outQuart`, `outQuint`, `outExpo`, `outCirc` | Increasingly dramatic. |
| `outBack` / `inBack` / `inOutBack` | Overshoots. Playful only. |
| `outElastic` / `inElastic` | Bouncy spring. Use sparingly. |
| `outBounce` / `inBounce` | Like a ball bouncing. |
| `inOut(N)` / `out(N)` / `in(N)` | **NEW in v4** — parametric power easings. `inOut(2)` is quad, `out(3)` is cubic-out, etc. |
| `steps(N)` | Discrete steps — for typewriter, ticker effects. |
| `irregular(steps, randomness)` | Steps with randomness — glitch effects. |
| `cubicBezier(x1, y1, x2, y2)` | Custom bezier — for designer-specified curves. |
| `createSpring({ mass, stiffness, damping, velocity })` | Physics-based spring. Returns an ease function. |

Parametric easings (`inOut(N)`) are a v4 superpower — replace `'easeInOutQuad'` with `'inOut(2)'`, `'easeInOutCubic'` with `'inOut(3)'`, etc.

```js
// Spring
animate('.box', {
  translateY: -50,
  ease: createSpring({ mass: 1, stiffness: 120, damping: 14 }),
});
```

## Global speed control

```js
animate.engine.speed = 0.5;     // half speed for all animations on the page
animate.engine.speed = 2;       // double speed
```

Set BEFORE creating timelines for the change to apply to new instances. For per-instance control:

```js
const tl = createTimeline({ ... });
tl.speed = 0.5;     // affects just this timeline
```

## Common v4 pitfalls (the ones that silently break widgets)

### Delay-only `.add()` does NOT exist

In v3 you could `tl.add({ duration: 1000 })` as a pure delay. **In v4 this silently does nothing useful** — the first argument is always a target. Trying to use it as a delay anchor makes the timeline appear ~3× faster than designed.

```js
// ❌ BAD — Anime.js treats {duration: 1000} as a target object, animates nothing.
tl.add({ duration: 1000 }, {}, "+=0")
  .call(() => doSomething());

// ✅ GOOD — use a label with offset
tl.label("hold-" + i, "+=1000")
  .call(() => doSomething(), "hold-" + i);

// ✅ ALSO GOOD — push the offset into the next .add()
tl.add(target, { ...params }, "+=1000");
```

### Pre-set transforms in CSS conflict with `animate(...)` transforms

If you write `.box { transform: scale(0.9); }` in CSS and then animate the same target with `animate('.box', { translateY: [6, 0] })`, **Anime.js takes over the transform property entirely and the initial `scale(0.9)` is discarded** the moment the animation starts. The element jumps to `scale: 1` at frame 0.

```js
// ❌ BAD — CSS has `transform: scale(0.9)`, then this is the first animation:
animate('.token', { translateY: [6, 0], duration: 350 });
// Next animation:
animate('.token', { scale: [0.9, 1.06, 1] });   // tries to scale-pop but starts from 1, not 0.9 → jumpy

// ✅ GOOD — set the initial state with utils.set(), then animate.
utils.set('.token', { opacity: 0, translateY: 6, scale: 0.9 });
animate('.token', { opacity: 1, translateY: 0, scale: [0.9, 1.06, 1], duration: 520 });
```

Rule: **never set transforms in CSS for elements Anime.js will animate**. Use `utils.set()` instead.

### Initial `opacity: 0` on classes that get re-used

If `.token-pill { opacity: 0; }` is used both for tokens (animated in by the timeline) AND for displaying static strings (NOT in the timeline's animated-targets selector), the static instances stay invisible forever.

```js
// ❌ BAD — selector misses the rawtext usage:
const animated = layer.querySelectorAll('.vector-block, .matrix, .heads');
//                                       ^^^^^^^^^^^ no .token-pill, but rawtext step uses .token-pill

// ✅ GOOD — either:
//   (a) Include every class that has initial opacity:0 in the selector, OR
//   (b) Remove the CSS opacity:0 and use opacity: [0, 1] from inside the animation
//   (c) Use a different class for non-animated text (e.g. `.raw-string`)
```

### `kind` switch in viz selector must cover every viz-kind

When the timeline animates per-step depending on `step.viz.kind`, a missing case leaves that step's visualization unanimated:

```js
// ❌ BAD — "residual" cells stay at scaleY: 0.2 because the kind isn't covered:
if (kind === "vectors" || kind === "qkv") {
  tl.add(cells, { scaleY: [0.2, 1], ... });
}

// ✅ GOOD — list every kind that uses .cell:
if (["vectors", "qkv", "residual"].includes(kind)) {
  tl.add(cells, { scaleY: [0.2, 1], ... });
}
```

### Restart should NOT rebuild the DOM

Rebuilding the DOM on every Restart click leaks animation instances (their targets get detached but `animate.engine` still ticks them) and is slow.

```js
// ❌ BAD — every restart wipes innerHTML and re-renders.
function restart() { rebuild(); play(); }

// ✅ GOOD — only rebuild when the path actually changes.
function restart() {
  timeline.pause();
  timeline.seek(0);
  utils.set('.layer', { opacity: 1 });
  utils.set('.layer.active', {}, { remove: 'class' });   // or use classList.remove on each
  timeline.play();
}
function onPathChange() { rebuild(); }
```

## text.split() — the v4 killer feature

Split any text into lines / words / chars with full control over wrapping, cloning, accessibility.

```js
import { text, animate, stagger, createTimeline } from "https://esm.sh/animejs@4";

const split = text.split('h1', {
  lines: true,                        // split into lines (auto-detected)
  words: true,                        // split into words
  chars: true,                        // split into characters
  wrap: 'clip',                       // false | 'clip' (overflow:hidden) | 'visible'
  clone: 'top',                       // false | 'top' | 'right' | 'bottom' | 'left'
                                      //   duplicates each unit offset in that direction
                                      //   (for "flip up" / "reveal from above" effects)
  includeSpaces: false,               // animate space chars too
  accessible: true,                   // preserve original text for screen readers
  debug: false,                       // show alignment guides
});

// split.lines, split.words, split.chars — arrays of HTMLElement
animate(split.chars, {
  opacity: [0, 1],
  delay: stagger(30),
});

// addEffect — runs on init + on re-split (e.g. responsive)
split.addEffect((self) => {
  return createTimeline({ /* ... */ }).add(self.lines, { y: -10 });
});

// Manual control
split.refresh();                      // re-split (after font load, resize, etc)
split.revert();                       // restore original DOM
split.debug = true;                   // show alignment outlines
```

`text.split()` is essential for Pattern M (text effects). Used in social-media reels, hero copy reveals, scramble text effects, magnet/repel on hover.

## svg.createDrawable — line drawing

```js
import { svg, animate, stagger, createTimeline } from "https://esm.sh/animejs@4";

createTimeline()
  .add(svg.createDrawable('.line-v'), {
    draw: ['0 0', '0 1'],             // draw from 0% to 100%
    stroke: '#FF4B4B',
    duration: 1000,
  }, stagger(50));
```

Use for: progress bars, route reveals on maps, sound waves, sketched outlines. The `draw` property animates `stroke-dashoffset` + `stroke-dasharray` internally.

For motion along an SVG path:

```js
const path = svg.createMotionPath('#my-svg-path');
animate('.dot', {
  ...path,                            // expands to translateX, translateY, rotate
  duration: 2000,
  ease: 'linear',
});
```

## utils — utilities you'll actually use

```js
import { utils } from "https://esm.sh/animejs@4";

utils.$('.selector')                  // returns Array<HTMLElement> (NodeList → Array)
utils.set(target, { x: 100, y: 50 }) // instant set without animating
utils.get(target, 'x')                // read current animated value
utils.random(min, max, precision?)    // random float, optional decimals
utils.randomPick(['a', 'b', 'c'])     // pick one
utils.round(value, decimals)          // round to N decimals
utils.sync(callback)                  // run a function in sync with the engine
utils.shuffle(array)                  // Fisher-Yates shuffle in place
utils.snap(value, snapTo)             // snap to grid / nearest step
utils.lerp(a, b, t)                   // linear interpolate
utils.clamp(v, min, max)              // clamp to range
utils.mapRange(v, in1, in2, out1, out2)  // remap value across ranges
```

## eases — pre-built ease functions (named exports)

```js
import { eases } from "https://esm.sh/animejs@4";

eases.inOutSine
eases.outQuart
eases.outBack
// etc — same names as the `ease` string values
```

Use the function directly when you need to compute progress in your own code:

```js
const t = eases.inOutSine(0.42);   // returns the eased value at 42% progress
```

## Animatable properties

| Type | Properties |
|---|---|
| Transforms | `translateX/Y/Z`, `rotate`, `rotateX/Y/Z`, `scale`, `scaleX/Y/Z`, `skewX/Y` |
| Shorthand alias | `x`, `y`, `z` (= translateX/Y/Z) |
| Opacity / color | `opacity`, `color`, `backgroundColor`, `fill`, `stroke` |
| Layout | `width`, `height`, `padding*`, `margin*`, `top`, `left`, `borderRadius` |
| Strokes | `strokeWidth`, `strokeDashoffset`, `strokeDasharray` |
| SVG attrs | `cx`, `cy`, `r`, `x1`, `y1`, `x2`, `y2`, `d` (for path morphing), `points` (polygon) |
| Custom props | `--my-css-var` (animate CSS variables directly) |
| Numeric text | `innerHTML` (animate text content as a number with `modifier: utils.round(0)`) |

## Numeric / counter animations

```js
animate('.count', {
  innerHTML: [0, 50000],                // animate from 0 to 50000
  modifier: utils.round(0),             // round to integer each frame
  duration: 4000,
  ease: 'cubicBezier(1,0,1,1)',         // exponential-like ramp
});
```

Combine with `loop`, `alternate`, etc for the "star counter going crazy" effect (Anime.js timeline 50K stars demo).

## Callbacks (per animation)

```js
animate('.x', {
  translateX: 100,
  onBegin:    self => {},               // first frame
  onUpdate:   self => { self.progress },// every frame
  onComplete: self => {},               // last frame
  onLoop:     self => {},               // each loop iteration boundary
});
```

`self` is the Animation/Timeline instance, with `.progress`, `.currentTime`, `.duration`, `.paused`, `.completed`, `.iterationCount`, `.speed`.

## Playback control

```js
const a = animate('.x', { translateX: 100, autoplay: false });

a.play();
a.pause();
a.restart();          // = pause + seek(0) + play
a.reverse();          // toggle direction
a.seek(500);          // jump to t=500ms (within the animation duration)
a.progress = 0.5;     // jump to 50% (alternative to seek)
a.refresh();          // re-read CSS values (use when window resized, fonts loaded, etc)
a.completed;          // boolean
a.duration;           // total ms
a.currentTime;        // current ms
```

## Common gotchas (v4 specific)

1. **`anime({})` doesn't exist anymore** — use `animate(targets, params)`.
2. **`easing` was renamed to `ease`.** v3 code with `easing: 'easeInOutSine'` becomes `ease: 'inOutSine'`.
3. **Built-in easing prefixes dropped.** `easeInOutSine` → `inOutSine`, `easeOutQuad` → `outQuad`. Just remove the `ease` prefix.
4. **`anime.timeline()` doesn't exist** — use `createTimeline(params)`.
5. **`anime.stagger()` doesn't exist** — use the named import `stagger`.
6. **Targets-first call signature.** v3 was `anime({ targets: '.x', ... })`. v4 is `animate('.x', { ... })`.
7. **`text.split()` is brand new in v4** — not available in v3.
8. **Speed setter changed.** v3: `anime.speed = 0.5`. v4: `animate.engine.speed = 0.5` (or per-timeline `.speed`).
9. **No more `anime.set()`** — use `utils.set()`.
10. **No CDN auto-globals.** v4 is ESM-only — you MUST use `<script type="module">` + named imports.

## Migration from v3

If you find code with `anime({ targets, ... })` it's v3. Quick conversion:

```diff
- import anime from "https://cdn.jsdelivr.net/npm/animejs@3";
+ import { animate, createTimeline, stagger } from "https://esm.sh/animejs@4";

- anime({ targets: '.box', translateX: 100, easing: 'easeInOutSine' });
+ animate('.box', { translateX: 100, ease: 'inOutSine' });

- const tl = anime.timeline({ easing: 'easeInOutQuad' });
+ const tl = createTimeline({ defaults: { ease: 'inOutQuad' } });

- delay: anime.stagger(100)
+ delay: stagger(100)

- anime.set(el, { x: 100 })
+ utils.set(el, { x: 100 })

- anime.speed = 0.5
+ animate.engine.speed = 0.5
```

## Resources

- Official site: <https://animejs.com>
- v4 docs: <https://animejs.com/documentation>
- Easing editor: <https://animejs.com/easing-editor>
- Examples: <https://animejs.com/showcase>
- ESM CDN: <https://esm.sh/animejs@4>
- npm: `npm install animejs`
