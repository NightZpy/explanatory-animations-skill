# Pattern O — Shape morph / layered transforms

## Use when

- Hero / loop animations for landing pages
- Abstract visualizers for music, podcast openers, motion posters
- Logo morphing between states
- "Generative" backgrounds for creator content
- Idle loops that play forever in the background
- Visual rhythm for ambient screens / digital signage

## Don't use when

- The shapes carry semantic meaning (use a labeled pattern instead)
- The animation needs to teach something specific — too abstract for didactic use

## Inputs the user must provide

```js
{
  shapes: [
    { type: "circle",  initial: { r: 32, color: "#FF4B4B" } },
    { type: "rect",    initial: { width: 48, height: 48 } },
    { type: "polygon", initial: { points: [[48,17.28],[86.4,80.12],[9.6,80.12]] } },
  ],
  motion: "drift",       // O.1 drift | O.2 morph | O.3 pulse | O.4 rotate-cascade
  duration: 1200,        // base — actual varies via keyframes
  loop: true,
  layered: true,         // stack shapes on top of each other
}
```

## O.1 — Drift + rotate + scale (Anime.js "Layered transforms" demo)

Three SVG shapes (circle, rect, triangle) overlap and continuously drift around their origin, with size + rotation + position all varying randomly:

```js
import { createTimeline, utils, createSpring } from "https://esm.sh/animejs@4";

const eases = ['inOutQuad', 'inOutCirc', 'inOutSine', createSpring()];

function createKeyframes(value) {
  const keyframes = [];
  for (let i = 0; i < 100; i++) {
    keyframes.push({
      to: value,
      ease: utils.randomPick(eases),
      duration: utils.random(300, 1600),
    });
  }
  return keyframes;
}

function animateShape(el) {
  const animation = createTimeline({
    onComplete: () => animateShape(el),   // restart with new randomized keyframes
  })
    .add(el, {
      translateX: createKeyframes(() => utils.random(-4, 4) + 'rem'),
      translateY: createKeyframes(() => utils.random(-4, 4) + 'rem'),
      rotate: createKeyframes(() => utils.random(-180, 180)),
    }, 0);

  const circle = el.querySelector('circle');
  if (circle) animation.add(circle, { r: createKeyframes(() => utils.random(24, 56)) }, 0);

  const rect = el.querySelector('rect');
  if (rect) animation.add(rect, {
    width:  createKeyframes(() => utils.random(56, 96)),
    height: createKeyframes(() => utils.random(56, 96)),
  }, 0);

  const poly = el.querySelector('polygon');
  if (poly) animation.add(poly, {
    points: createKeyframes(() => {
      const s = utils.random(.9, 1.6, 3);
      return `${48*s} ${17.28*s} ${86.4*s} ${80.12*s} ${9.6*s} ${80.12*s}`;
    }),
  }, 0);

  animation.init();
}

document.querySelectorAll('.shape').forEach(animateShape);
```

The signature trick: **100 randomized keyframes per property**, each with a different ease — the motion feels organic, never repeats, never hits a "loop" point the eye notices.

## O.2 — Polygon morph (between geometric shapes)

Animate the `points` attribute of an SVG polygon directly:

```js
animate('polygon', {
  points: [
    '48 17 86 80 10 80',          // triangle
    '24 24 72 24 72 72 24 72',    // square
    '48 10 86 48 48 86 10 48',    // diamond
    '48 17 86 80 10 80',          // back to triangle
  ],
  duration: 3000,
  loop: true,
  ease: 'inOutSine',
});
```

Each polygon string must have the **same number of points** for smooth interpolation. Pad with duplicate points if needed (e.g. triangle → square needs 4 points on each).

## O.3 — Pulse (in/out scaling loop)

```js
animate('.shape', {
  scale: [1, 1.15, 1],
  duration: 1800,
  loop: true,
  ease: 'inOutSine',
  delay: stagger(200, { from: 'center' }),
});
```

Centered stagger creates a ripple — useful for sound visualizers, loading screens.

## O.4 — Rotate cascade (geometric mandala feel)

```js
animate('.shape', {
  rotate: 360,
  duration: 4000,
  loop: true,
  ease: 'linear',
  delay: stagger(400),
});
```

Each shape rotates at its own pace — combined with O.1's translation, creates intricate moving mandalas.

## O.5 — Path morph (SVG `<path>` `d` attribute)

For organic shapes (blobs, waves):

```js
animate('path', {
  d: [
    'M 50 80 Q 100 50 150 80 T 250 80',
    'M 50 80 Q 100 120 150 80 T 250 80',
    'M 50 80 Q 100 50 150 80 T 250 80',
  ],
  duration: 2000,
  loop: true,
  ease: 'inOutSine',
});
```

For complex morphs (logo → logo), use the [flubber](https://github.com/veltman/flubber) library to generate intermediate path strings.

## Variants

- **Color animation** — add `fill` or `stroke` to the keyframes so shapes shift color as they morph.
- **Stagger across many shapes** — `stagger(50)` on the keyframes themselves to ripple the morph.
- **Reactive to audio** — drive parameters via WebAudio analyzer node (frequency bins → scale / rotation).
- **Mouse-reactive** — replace `random` with cursor-driven values for an interactive hero.

## Pitfalls specific to O

1. **Forgetting `transform-box: fill-box`** on SVG elements — they rotate around the page origin instead of their own center. Set `transform-box: fill-box; transform-origin: center;` on `<rect>`, `<circle>`, `<polygon>`.
2. **All shapes synchronized** — looks robotic. The whole point of O is non-determinism via random keyframes.
3. **Heavy keyframe arrays in `loop: true`** — anime.js v4 handles them well, but for >300 simultaneous keyframes consider WebGL.
4. **No `will-change: transform`** on the host element — janky on Safari.
5. **Polygons with different point counts** in O.2 — anime.js falls back to linear text interpolation which looks broken.
6. **Animating `width`/`height` on a `<rect>`** during heavy motion is slow — prefer scaling via `scaleX`/`scaleY` when possible.

## Recommended container CSS

```css
.shape-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 16rem;
  height: 16rem;
  transform: scale(1.75);
  /* shapes will overlap inside via position: absolute */
}
.shape {
  position: absolute;
  overflow: visible;
  width: 8rem;
  height: 8rem;
  stroke: currentColor;
  fill: transparent;
  will-change: transform;
}
.shape polygon, .shape rect, .shape circle {
  transform-box: fill-box;
  transform-origin: center;
}
```
