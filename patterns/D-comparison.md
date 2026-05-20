# Pattern D — Side-by-side comparison

## Use when

- Two approaches contrasted: with/without cache, push vs pull, locked vs lock-free, sync vs async
- Before/after refactor showing a performance delta
- Two algorithms solving the same problem (bubble sort vs quick sort)
- Two architectures handling the same request (monolith vs microservices)

## Don't use when

- More than 2 things to compare — use a single animation with multiple paths instead
- The comparison is qualitative (e.g. "X is more elegant") — better as prose

## Inputs the user must provide

```js
{
  title: "With vs without cache",
  metric: { unit: "ms", lowerIsBetter: true },
  left:  { name: "Without cache", animation: /* pattern A or B config */, expectedMs: 1200 },
  right: { name: "With cache",    animation: /* pattern A or B config */, expectedMs: 220  },
}
```

## Visual structure

- Two identical stages side by side (50/50 width, or stacked on mobile).
- Same animation runs in both — same packet style, same easing, same cards.
- One **synchronized Play button** drives both timelines as children of a single anime.js master timeline.
- Below each stage: the metric (elapsed ms / # of network calls / # of disk reads), updating in real time.
- Below both stages: a winner pill ("3× faster") that appears when both timelines complete.

## Animation choreography

1. Play clicked → both timelines start simultaneously.
2. Left side reaches completion at e.g. 1200ms.
3. Right side reaches completion at e.g. 220ms — much earlier.
4. Right side's "finished" pill appears; left side continues, building suspense.
5. Left side finishes; the winner pill appears with the delta.

## Variants

- **Hold the faster side in place** — once one finishes, freeze it with a checkmark while the other still plays.
- **Per-step metric** — show ms ticking up next to each card as the packet arrives.
- **Replay individually** — small "play just this side" buttons under each stage for closer inspection.

## Pitfalls

1. **Different easings between sides** — they should be identical so the only difference is the path length / # of stops.
2. **Same metric label not visible** — readers must see "ms" or "RTTs" or whatever the metric is, BIG and right under each stage.
3. **Winner declared mid-flight** — wait until both finish to show the winner pill, otherwise it spoils the suspense.
4. **Left side always the "bad" one** — vary placement; sometimes the new approach is on the right, sometimes the left.
