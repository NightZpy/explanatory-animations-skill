# Pattern H — Particle flow

## Use when

- Network packet flow between many endpoints
- Data flow through ETL: many records per second
- Water / fluid in plumbing diagrams
- Traffic / migration / commuter flow on a map
- Electrons / charge in a circuit

## Don't use when

- Only one packet matters — use **B (system flow)** with a single packet
- The particles are doing different things — use **B** with multiple paths

## Inputs the user must provide

```js
{
  title: "Logs flowing into OpenObserve",
  sources:  [{ id: "api", x: 100, y: 100 }, { id: "web", x: 100, y: 200 }, { id: "worker", x: 100, y: 300 }],
  sinks:    [{ id: "oo",  x: 600, y: 200 }],
  paths: [
    { from: "api",    to: "oo", via: [{x: 350, y: 100}, {x: 350, y: 200}] },
    { from: "web",    to: "oo", via: [{x: 350, y: 200}] },
    { from: "worker", to: "oo", via: [{x: 350, y: 300}, {x: 350, y: 200}] },
  ],
  density: 8,    // particles per second per source
  particleRadius: 3,
  duration: 2500, // ms one particle takes source-to-sink
}
```

## Visual structure

- Static elements: source boxes and sink boxes (drawn once).
- Static path lines: thin gray lines showing the route particles will follow.
- Particles: small `<circle>`s spawning at sources at a steady cadence, flowing along the path.
- Sink: each particle disappears (fades + scale-down) at the sink.

## Animation choreography

This pattern uses **anime.js `stagger` + infinite loop**. Spawn N particles staggered by `1000/density` ms; each one runs the same source-to-sink animation.

```js
sources.forEach(source => {
  setInterval(() => spawnParticle(source), 1000 / density);
});

function spawnParticle(source) {
  const circle = createCircle();
  source.svg.appendChild(circle);
  anime({
    targets: circle,
    keyframes: pathVia(source).map(pt => ({ cx: pt.x, cy: pt.y })),
    duration: cfg.duration,
    easing: "linear",
    complete: () => circle.remove(),
  });
}
```

For paths longer than ~6 segments, use SVG `<path>` + anime's `motionPath` helper.

## Variants

- **Density slider** — let the user drag from "1 packet/s" up to "100 packets/s" to see how the system handles load.
- **Color by source** — each source emits a different color particle, so the eye can trace which source contributed which.
- **Backpressure visual** — when sinks can't keep up, particles bunch up at the sink with a queue indicator.
- **Click to spawn one** — interactive mode where each click sends a single particle.

## Pitfalls

1. **Particles all spawning at t=0** — they line up like a comb. Stagger spawn over `1000/density` ms.
2. **All particles same speed** — looks robotic. Add `±10%` jitter to `duration`.
3. **Memory leak** — always `circle.remove()` in `complete`. With 8 p/s sustained, leaking circles crashes the page in a minute.
4. **Canvas vs SVG** — for >300 simultaneous particles, switch to Canvas (`<canvas>` + `requestAnimationFrame`). SVG handles ≤300 fine.
5. **Source boxes that don't visibly emit** — add a small pulse at the source each time a particle spawns, so the source feels like the cause.
