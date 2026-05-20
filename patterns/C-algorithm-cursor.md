# Pattern C — Cursor over data structure

## Use when

- Sorting algorithms (bubble, quick, merge, insertion, selection)
- Search (binary search, linear search)
- Tree operations (BST insert, AVL rotation, B-tree split)
- Hash table operations (collision, resize)
- Graph traversal (BFS, DFS, Dijkstra)

## Don't use when

- The structure doesn't visually exist (e.g. abstract recurrences) — use **E (math reveal)**
- Multiple structures interact — use **B (system flow)** with each structure as a subsystem

## Inputs the user must provide

```js
{
  title: "Bubble sort",
  structure: { kind: "array", values: [5, 2, 8, 1, 9, 3] },
  operations: [
    { type: "compare", i: 0, j: 1 },
    { type: "swap",    i: 0, j: 1 },
    { type: "compare", i: 1, j: 2 },
    // ...
  ],
  variables: ["i", "j"],   // tracked next to the structure
}
```

## Visual structure

- Top: the structure itself, persistent (array cells as `<rect>`s, tree nodes as labeled circles).
- Cursor: a colored outline + small caret pointing at the active cell.
- Side panel: current step number, current variables (`i=3, j=5`), action log of completed steps.
- The structure stays visible the whole time — cells change color, never disappear.

## Animation choreography

1. Cursor moves to operation target — 400ms.
2. 300ms pause — highlight the involved cells.
3. Action fires (swap = exchange positions with crossfade, compare = both cells pulse, insert = new cell slides in pushing others).
4. 400ms after — cursor moves on, log appends.

## Variants

- **Step-through mode** (recommended for algorithms) — manual ⏮ ⏭ buttons replace auto-play. Each click advances one operation.
- **Visualize complexity** — show a small counter "comparisons: 12 / swaps: 4" updating per operation.
- **Pseudo-code panel** — three lines of code next to the structure, current line highlighted as the cursor moves.

## Pitfalls

1. **Animating the structure into existence** — start with it fully visible. Animation is for changes, not introduction.
2. **Swap as instant snap** — should be a smooth crossfade so the eye tracks both cells.
3. **No variable display** — algorithms with `i`, `j`, `pivot` are unreadable without showing the current values.
4. **Cursor too small** — make it bold; readers need to find it instantly.
