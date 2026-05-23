# Pattern I — Layered transformation

## Use when

- How an LLM processes input: tokens → embeddings → attention → output
- Neural network forward pass: input layer → hidden layers → output layer
- Image processing pipeline: raw → demosaic → denoise → tone-map → encode
- Compiler stages: source → AST → IR → assembly → machine code
- Encryption rounds (AES, RSA): plaintext → permute → S-box → mix → ciphertext
- Audio processing: PCM → DFT → filter → IDFT → output

## Don't use when

- The data shape doesn't change per layer — use **B (system flow)** instead
- Only one layer matters — use **C (cursor)** or single-card animation

## Inputs the user must provide

```js
{
  title: "LLM forward pass",
  input: { kind: "text", value: "Cats are awesome" },
  layers: [
    { name: "Tokenizer",       output: { kind: "tokens",     value: ["Cats", " are", " awesome"] } },
    { name: "Embeddings",      output: { kind: "vectors",    value: [[768], [768], [768]] } },
    { name: "Attention 1",     output: { kind: "vectors",    value: [[768], [768], [768]] }, sublayers: ["Q×K", "softmax", "×V"] },
    { name: "FFN 1",           output: { kind: "vectors",    value: [[768], [768], [768]] } },
    { name: "Attention 2..N", output: { kind: "vectors",    value: [[768], [768], [768]] } },
    { name: "LM head",         output: { kind: "logits",     value: [0.1, 0.05, 0.7, ...] } },
    { name: "Sampling",        output: { kind: "token",      value: "!" } },
  ],
  showVectorShapes: true,    // visualize the data shape: tokens as text, vectors as colored bars
}
```

## Output mode — pick BEFORE building

Pattern I works in **both** browser-native and video-target modes, but the layout is fundamentally different. Decide in step 5a of the discovery (see [`../library/output-modes.md`](../library/output-modes.md)).

### Browser-native (default for didactic use)

- Vertical stack of full-width layer cards, each card holds one layer's content + viz.
- Page scrolls; controls strip is sticky at the top.
- The "current data" indicator is a colored left-border on the active card, or a small avatar that descends inline.
- Total page height grows with `cardCount × cardHeight`.
- **Cannot be exported to video cleanly** — recording captures a long scrollable WebM, unusable.

### Video-target (default when the user says "reel", "short", "post", or asks for an MP4)

- Stage is a **fixed-size frame** (1920×1080 / 1080×1920 / 1080×1080). No scroll.
- Layout splits into **overview sidebar (25-30%) + focal area (70-75%)**:
  - Overview: small list of layer names, the active one highlighted, line connecting them — gives spatial context without scrolling.
  - Focal area: the active layer's viz is **swapped in place** (previous fades out, next fades in) rather than appended.
- Layer descriptions are 1-2 short lines max. If the user provides paragraphs, summarize them or move them to a "transcript" overlay shown only when paused.
- Step count budget per 60s reel: ≤ 8 (8s per step including transitions). For 14-step zoom flows, either (a) chapter into a 2-part video, (b) speed up to 4s/step and accept that viewers will pause.

## Visual structure (browser-native)

- Vertical stack of layer cards, each with: name, sublayers (if any), and a small visualization of the data shape at its output.
- Data flows top-to-bottom (or left-to-right for wider screens).
- Between layers: a connector with the operation name ("→ tokenize", "→ embed", "→ attend").
- The "current data" badge follows the cursor as it descends through the layers.

## Visual structure (video-target)

- Fixed-size `.stage` with `data-export-target` for the Export button.
- Left column (25-30% width): vertical list of layer names, the active one in accent color, a small dot moves down as the layer changes.
- Right column (70-75% width): the focal area — title of current layer, 1-2 sentence description, in-place viz. When transitioning to the next layer, fade out + fade in the focal content (do NOT append below).
- Controls strip is OUTSIDE the stage, hidden during recording via `?clean=1`.

## Animation choreography

1. Input appears at the top, fully rendered.
2. Cursor descends into layer 1. Layer 1 expands (height grows), shows its sublayers.
3. As the cursor moves through each sublayer, a small operation visual plays (e.g. for attention: matrix-multiply visual).
4. Layer 1 closes (collapse to its rest height), the output appears at its bottom edge.
5. Cursor descends to layer 2. Repeat.
6. Final layer outputs the result (e.g. a sampled token).

## Variants

- **LLM internals (specific)** — show actual matrix shapes (768-dim vectors, attention heads, weight matrices) and color-coded by their role.
- **Neural net forward pass** — layers are dense / conv / pool; show activations as heatmaps.
- **Compiler stages** — show the actual textual representation transforming (source code → tokens → AST → IR strings).
- **Step-by-step zoom** — clicking a layer expands it into its own widget (sub-animation of just that layer).

## Pitfalls

1. **Showing all layers static, no animation** — that's a diagram, not an animation. Animate the cursor descending and each layer expanding/collapsing.
2. **Vector shapes shown as just numbers** — visualize them (colored bars, sparkline, mini-heatmap) so the eye sees the shape change.
3. **No "current data" follower** — readers lose track of what's being transformed.
4. **Equal time per layer** — important layers (attention, sampling) deserve more time. Make layer durations configurable.
5. **No final output emphasis** — the resulting token / pixel / instruction should appear with extra weight (larger, glowing, "popped out").
6. **Building browser-native then trying to export to video** — the scrollable layout produces a long thin WebM, unusable. Pick the output mode in step 5a, never retrofit. If the user changes their mind, regenerate from scratch.
7. **Video-target layout that allows scroll inside the stage** — if content overflows the fixed frame, the layout is wrong. Re-architect: fewer layers per frame, smaller in-card viz, or split into a multi-part reel. Never let `.stage` have `overflow: auto` or unbounded height.
8. **First layer's viz uses a class that has initial `opacity: 0` from CSS, but the timeline's selector doesn't include it.** Result: the first step appears empty, animation feels like it "doesn't start". See mistake #11 in `_mistakes.md`. Audit every viz-kind to make sure its container is animated.
9. **`viz.kind` cases that share a class but not the kind-switch.** Residual / vectors / qkv all use `.vector-row .cell` but only some are listed in the `cells` animation selector → unlisted ones show as flat lines. See mistake #14.
10. **Restart rebuilds the DOM on every click instead of `pause + seek(0) + utils.set`.** Leaks animation instances. See mistake #15. Rebuild only on path change.
