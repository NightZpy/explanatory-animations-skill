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

## Visual structure

- Vertical stack of layer cards, each with: name, sublayers (if any), and a small visualization of the data shape at its output.
- Data flows top-to-bottom (or left-to-right for wider screens).
- Between layers: a connector with the operation name ("→ tokenize", "→ embed", "→ attend").
- The "current data" badge follows the cursor as it descends through the layers.

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
