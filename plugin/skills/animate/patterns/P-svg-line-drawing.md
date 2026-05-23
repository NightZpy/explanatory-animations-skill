# Pattern P — SVG line drawing

## Use when

- Sound waves (audio visualizer, podcast intro, radio metaphor)
- Maps drawing themselves (route reveal, border outline)
- Sketch-on reveal (logo, signature, illustration)
- Wave patterns for science / fluid dynamics
- ECG / pulse / heartbeat visualizers
- Spirograph / parametric curves for ambient backgrounds
- Math curves (sine, cosine, parabolas) tracing themselves
- Architectural blueprints animating in

## Don't use when

- The line is meant to convey data semantics — use a chart library
- Too much path complexity (>1000 segments) — switch to canvas

## Inputs the user must provide

```js
{
  paths: [
    { id: "circle-1", d: "M 50 50 L 250 50" },
    // ... or programmatically generated paths (see "SVG line drawing" demo)
  ],
  drawOrder: "sequential" | "stagger" | "simultaneous",
  staggerMs: 50,
  duration: 1200,
  stroke: "#A4FF4F",
  strokeWidth: 4,
  variant: "draw-on" | "trace" | "morph-stroke" | "wave",
}
```

## P.1 — Draw-on (line reveals itself from start → end)

```js
import { svg, animate, stagger, createTimeline } from "https://esm.sh/animejs@4";

createTimeline()
  .add(svg.createDrawable('.line-v'), {
    draw: ['0 0', '0 1'],          // animate from 0% drawn to 100% drawn
    stroke: '#A4FF4F',
    duration: 1000,
    ease: 'inOut(4)',
  }, stagger(50));
```

`svg.createDrawable()` measures the path length and sets up `stroke-dasharray` + `stroke-dashoffset` so the `draw` property animates clean line revealing. Works on `<line>`, `<path>`, `<polyline>`, `<circle>`, `<rect>`, `<ellipse>`, `<polygon>`.

The `draw` value is a string `"<from> <to>"` where each is 0..1 representing % of the path length.

## P.2 — Trace (a "head" travels along, leaving a trail behind)

```js
animate(svg.createDrawable('#path'), {
  draw: [
    () => `${utils.random(0, .25, 2)} ${utils.random(.5, .75, 2)}`,
    () => `${utils.random(0, .5, 2)} ${utils.random(.5, 1, 2)}`,
    () => `${utils.random(0, .75, 2)} ${utils.random(.75, 1, 2)}`,
  ],
  stroke: '#FF4B4B',
  duration: 8000,
  loop: true,
  ease: 'inOut(2)',
});
```

The head + tail both move (changing the `from` and `to` parts of `draw`). Use for: traveling waves, comet trails, ECG sweep.

## P.3 — Sound wave (many vertical lines, each one breathing)

The "SVG line drawing" Anime.js demo generates 100 vertical lines + 50 concentric circles, then animates each one's `draw` independently — creating an audio-visualizer-like ripple.

```js
function generateLines(numberOfLines, svgWidth = 1100, svgHeight = 1100) {
  const margin = 50;
  const spacing = (svgWidth - margin * 2) / (numberOfLines - 1);
  let svgContent = `<svg viewBox="0 0 ${svgWidth} ${svgHeight}"><g id="lines">`;
  for (let i = 0; i < numberOfLines; i++) {
    const x = margin + i * spacing;
    svgContent += `<line x1="${x}" y1="${margin}" x2="${x}" y2="${svgHeight - margin}" class="line-v" stroke="#A4FF4F" stroke-width="10"/>`;
  }
  svgContent += `</g></svg>`;
  return svgContent;
}
document.body.insertAdjacentHTML('beforeend', generateLines(100));

createTimeline({ defaults: { ease: 'inOut(4)', duration: 10000, loop: true } })
  .add(svg.createDrawable('.line-v'), {
    draw: [
      '.5 .5',                              // start hidden (zero-length range at midpoint)
      () => { const l = utils.random(.05, .45, 2); return `${.5 - l} ${.5 + l}`; },
      '0.5 0.5',
    ],
    stroke: '#FF4B4B',
  }, stagger([0, 8000], { start: 0, from: 'first' }));
```

`stagger([0, 8000])` spreads the start time of each line from 0 to 8s — creating a continuous wave across the line grid.

## P.4 — Concentric circles (radio waves, sonar pulses)

```js
function generateCircles(n, cx, cy, maxR) {
  const step = maxR / n;
  let svg = `<svg viewBox="0 0 1100 1100"><g id="circles">`;
  for (let i = 0; i < n; i++) {
    svg += `<circle class="circle" cx="${cx}" cy="${cy}" r="${(i + 1) * step}" fill="none" stroke="#A4FF4F" stroke-width="10"/>`;
  }
  svg += `</g></svg>`;
  return svg;
}

animate(svg.createDrawable('.circle'), {
  draw: ['0 0', '0 1', '1 1'],
  stroke: '#FF4B4B',
  duration: 8000,
  loop: true,
}, stagger([0, 8000]));
```

Effect: concentric rings expanding outward like a sonar ping or radio broadcast.

## P.5 — Sine wave traced live (math visualization)

```html
<svg viewBox="0 0 600 200"><path id="sine" d="" stroke="#22d3ee" stroke-width="3" fill="none"/></svg>
```

```js
function sinePath(t) {
  let d = `M 0 100`;
  for (let x = 0; x <= 600; x += 4) {
    const y = 100 + Math.sin((x / 600) * Math.PI * 4 + t) * 40;
    d += ` L ${x} ${y}`;
  }
  return d;
}

const startT = performance.now();
function tick() {
  const t = (performance.now() - startT) / 500;
  document.getElementById('sine').setAttribute('d', sinePath(t));
  requestAnimationFrame(tick);
}
tick();
```

Use `requestAnimationFrame` directly for this — anime.js is overkill when you're literally redrawing every frame.

## P.6 — Logo / signature reveal

Take an SVG logo, treat each `<path>` as a stroke, draw them on with stagger:

```js
animate(svg.createDrawable('.logo path'), {
  draw: ['0 0', '0 1'],
  stroke: '#000',
  fill: { from: 'transparent', to: '#000' },     // fill in after stroke completes
  duration: 1500,
  delay: stagger(150),
  ease: 'inOutQuad',
});
```

Make sure the SVG uses individual `<path>` elements (not a single complex path) for the stagger to look right.

## Variants

- **Stop on tap** — change `loop` to a controllable timeline with pause/play.
- **Color cycle** — animate `stroke` through 3-4 colors during the draw.
- **Variable stroke width** — keyframes on `strokeWidth` `[0, 20, 20, 20, 0]` for fade-in / fade-out.
- **Wave intensity tied to audio** — drive the wave amplitude from WebAudio analyzer.
- **2D mesh** — combine P.3 lines + P.4 circles for grid-like field visualizers.

## Pitfalls specific to P

1. **Forgot `fill="none"`** on the SVG — line draws but is filled behind, looks wrong.
2. **No `stroke-linecap`** — line ends are square by default. Add `stroke-linecap="round"` for polished look.
3. **`pathLength` unset on weird paths** — `svg.createDrawable` measures it for you, but if you compute manually, set `pathLength="100"` so `dasharray` is predictable.
4. **Animating `d` with different point counts** — anime.js falls back to text-interpolation which can produce broken intermediate strings. Pad both sides to same point count.
5. **Animating `strokeDashoffset` directly** instead of using `svg.createDrawable` — works but you have to compute the length yourself. Just use the helper.
6. **100+ simultaneous lines on Safari** — Safari has issues with large `<g>` SVGs. Test there or fall back to canvas.

## Recommended SVG setup

```svg
<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <path
    d="M 50 100 Q 300 50 550 100"
    stroke="#A4FF4F"
    stroke-width="4"
    stroke-linecap="round"
    stroke-linejoin="round"
    fill="none"
  />
</svg>
```
