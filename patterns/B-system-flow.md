# Pattern B — System flow (ByteByteGo style)

## Use when

- HTTP request: browser → CDN → load balancer → app server → DB
- Microservices choreography: API → message broker → 3 consumers → external API
- ETL pipeline: source DB → CDC → Kafka → stream processor → warehouse
- Streaming architecture: ingestor → buffer → workers → store
- Anything with **multiple subsystems** organized into **architectural layers**

## Don't use when

- Only one entity progresses through states → use **A (lifecycle)**
- The interesting thing is timing on a literal axis → use **L (timeline)**
- The geography matters → use **J (geographic map)**

## Inputs the user must provide

```js
{
  layers: [
    { id: "client",    label: "Client & Edge",       color: "edge" },
    { id: "app",       label: "App Cluster",         color: "app"  },
    { id: "data",      label: "Data + Side-effects", color: "data" },
  ],
  nodes: [
    { id: "user", layer: "client", icon: "👤", name: "User",       sub: "browser" },
    { id: "cf",   layer: "client", icon: "☁️", name: "Cloudflare", sub: "DNS · SSL" },
    { id: "api",  layer: "app",    icon: "⚡", name: "API",         sub: "Fastify" },
    { id: "pg",   layer: "data",   icon: "🐘", name: "Postgres",    sub: "source of truth" },
    // ...
  ],
  edges: [
    { from: "user", to: "cf",  sf: "r", st: "l", label: "HTTPS",     num: 1 },
    { from: "cf",   to: "api", sf: "b", st: "t", label: "proxy",     num: 2 },
    { from: "api",  to: "pg",  sf: "b", st: "t", label: "SQL",       num: 3 },
  ],
  paths: {
    sync:   ["user→cf", "cf→api", "api→pg"],
    async:  /* alt sequence */,
  },
}
```

`sf` / `st` are "side of from" / "side of to" ∈ {`l`, `r`, `t`, `b`}. Orthogonal arrows derive from these.

## Visual structure

- CSS Grid layout: `grid-template-columns: 1fr 1fr 1fr` (or however many vertical lanes)
- Layers as **boundary regions** — a `<div>` spanning all columns of its rows, with dashed border + 5% alpha background gradient
- Nodes positioned in grid cells, white cards with icon + name + subtitle
- SVG overlay (`position: absolute; inset: 0; pointer-events: none`) holds:
  - `<path>` per edge (orthogonal, 90° bends only)
  - Numbered `<g class="step-badge">` at the bend point of main-path edges
  - `<rect>` + `<text>` edge labels with white background
  - Animated packet `<circle>`

## Animation choreography

1. **Build** — measure all node positions via `getBoundingClientRect`. Render arrows orthogonal between attach points.
2. **Play** — source node lights up. Packet appears at source.
3. **Per edge** — light up the edge (mute → lit/sync color), light the numbered badge, walk the packet along each segment of the orthogonal path (linear easing per segment, 420ms each).
4. **On arrival** — mark destination active (scale 1.06, amber inset ring), previous goes to "visited" (subtle outline).
5. **Done** — packet fades.

## Anime.js skeleton

```js
// Path is multi-segment — walk segment-by-segment
for (let i = 1; i < pts.length; i++) {
  tl.add({ targets: packet, cx: pts[i].x, cy: pts[i].y, duration: 420, easing: "linear" });
}
tl.add({ duration: 80, complete: () => {
  prev.classList.add("visited"); cur.classList.add("active");
  anime({ targets: cur, scale: [1, 1.1, 1.06], duration: 360, easing: "easeOutQuad" });
}});
```

## Variants

- **Single path** (sync request only) — minimal, no path selector
- **Multi-path with color coding** — different paths in different colors (amber default, blue sync, rose side-effects)
- **Bidirectional response** — animate the response packet coming back, with a different color
- **Failure injection** — add a "force failure on hop X" toggle that replaces the success path mid-flight

## Pitfalls specific to B

1. **Diagonal arrows.** Real ByteByteGo never uses them. If your layout makes a diagonal necessary, the layout is wrong.
2. **Edge labels without backgrounds.** They overlap the arrow line and become unreadable. Always wrap label `<text>` in a white `<rect>`.
3. **Bend point not on a grid intersection.** Arrows that bend in mid-air look amateurish. Orthogonal bends happen at integer multiples of half-grid step.
4. **Reusing layer colors across non-adjacent layers.** Each layer gets a unique color from `library/colors.md`.
5. **Step number sequence skipping** — if your main path is `1, 2, 4`, you missed step 3. Always sequential 1..N.
