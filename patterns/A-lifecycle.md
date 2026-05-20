# Pattern A — Lifecycle / state machine

## Use when

- Job lifecycle: queued → active → completed | failed | retried
- Order status: placed → paid → shipped → delivered | refunded
- Feature flag rollout: off → 10% → 50% → 100% | rollback
- Bug ticket: new → triaged → in-progress → done | wont-fix
- Auth session: anonymous → logging-in → authenticated | expired

## Don't use when

- More than one actor / system is involved → use **B (system flow)**
- States change over a literal time axis → use **L (timeline)**
- Data is being transformed inside each state → use **I (layered transform)**

## Inputs the user must provide

```js
{
  title: "Job lifecycle",
  nodes: [
    { id: "queued",    label: "queued",    tone: "pending", x: 80,  y: 100 },
    { id: "active",    label: "active",    tone: "warn",    x: 260, y: 100 },
    { id: "completed", label: "completed", tone: "ok",      x: 460, y: 50  },
    { id: "failed",    label: "failed",    tone: "bad",     x: 460, y: 150 },
  ],
  edges: [
    ["queued","active"], ["active","completed"], ["active","failed"]
  ],
  paths: {
    happy:   ["queued","active","completed"],
    failure: ["queued","active","failed"],
  },
}
```

Required: `nodes`, `edges`, `paths`. Optional: `labels` (path display names), `viewBox` (default 720×240).

`tone` ∈ {`pending`, `warn`, `ok`, `bad`, `db`, `queue`, `external`, `edge`} — drives colors per [`library/colors.md`](../library/colors.md).

## Visual structure

```
                  ┌──────────┐
                  │ completed │
                  └──────────┘
                       ↑
┌────────┐    ┌────────┐
│ queued │ → │ active  │
└────────┘    └────────┘
                       ↓
                  ┌────────┐
                  │ failed │
                  └────────┘
```

- Nodes: `<rect rx=8 width=104 height=36>` + `<text>` inside SVG
- Edges: `<line>` with `marker-end="url(#arrow)"`
- Traveler: single `<circle r=7>` that walks the active path
- Tone of each node sets its fill + stroke + text colors

## Animation choreography

1. **At rest** — all nodes white with gray border. Traveler hidden (opacity 0).
2. **Play** — traveler appears at the source node. Source node lights up with its tone color.
3. **Per hop** — traveler moves to next node over 700ms easeInOutSine, with 200ms delay before each hop. As it crosses, the edge stroke changes to the destination tone.
4. **On arrival** — destination node fades in its tone fill + stroke + does a 320ms scale pulse (1 → 1.08 → 1.04).
5. **At terminal** — traveler fades out over 400ms.

## Anime.js skeleton

```js
const tl = anime.timeline({
  easing: "easeInOutSine",
  begin:    () => setStatus("playing", "playing"),
  complete: () => setStatus("done"),
});

for (let i = 1; i < sequence.length; i++) {
  const next = nodes.find(n => n.id === sequence[i]);
  tl.add({
    targets: dot,
    cx: next.x, cy: next.y,
    duration: 700, delay: 200,
    update: anim => { if (anim.progress > 10) edge.setAttribute("stroke", toneColor(next.tone)); },
    complete: () => highlightNode(next),
  });
}
tl.add({ targets: dot, opacity: 0, duration: 400, delay: 500 });
```

## Variants

- **Multi-traveler**: spawn 2-3 dots staggered by 600ms to show "lots of jobs flowing in parallel". Use this when the user asks "and at scale?".
- **Cycle / retry edges**: dashed line + traveler that goes back. Mark cycles with a small "↻" pill on the edge label.
- **Compact horizontal-only**: viewBox 720×80, all nodes on y=40, suitable for inline blog usage.
- **Vertical orientation**: rotate 90°, useful when the page is narrow.

## Pitfalls specific to A

1. **Putting the number inside the node card.** States get names, transitions get numbers. The number goes on the arrow.
2. **Failure as a path that's identical to happy except the last step.** Make failure paths visually distinct — color the last edge red, scale the failure node less (it's a dead end, don't celebrate it).
3. **Auto-playing without anyone watching.** If the widget is below the fold, defer auto-play to `IntersectionObserver` firing at 50% visibility.
