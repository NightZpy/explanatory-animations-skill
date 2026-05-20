# Pattern K — Cross-section / stack

## Use when

- OSI 7 layers — physical → data link → network → transport → session → presentation → application
- Memory hierarchy — registers → L1 → L2 → L3 → RAM → disk
- Storage stack — application → filesystem → block device → physical disk
- Geological strata, oceanographic layers (epipelagic → mesopelagic → bathypelagic)
- Web stack — HTML / CSS / JS / network / device
- Earth's atmosphere layers

## Don't use when

- The layers aren't literally stacked — use **I (layered transform)** instead
- More than 7 layers — split into a "cross-section" + a "detail" widget

## Inputs the user must provide

```js
{
  title: "OSI 7 layers",
  orientation: "vertical",  // or "horizontal"
  layers: [
    { id: "physical",     name: "Physical",     desc: "bits over the wire",       color: "#dbeafe" },
    { id: "datalink",     name: "Data Link",    desc: "frames between adjacent",  color: "#ddd6fe" },
    { id: "network",      name: "Network",      desc: "routing across networks",  color: "#fce7f3" },
    { id: "transport",    name: "Transport",    desc: "end-to-end reliability",   color: "#fed7aa" },
    { id: "session",      name: "Session",      desc: "session management",       color: "#fef3c7" },
    { id: "presentation", name: "Presentation", desc: "encoding, encryption",     color: "#dcfce7" },
    { id: "application",  name: "Application",  desc: "HTTP, SMTP, etc.",         color: "#cffafe" },
  ],
  flows: [
    { name: "Send a packet", direction: "down", traversal: ["application","presentation","session","transport","network","datalink","physical"] },
    { name: "Receive a packet", direction: "up", traversal: ["physical","datalink","network","transport","session","presentation","application"] },
  ],
}
```

## Visual structure

- Each layer as a wide horizontal `<rect>` (vertical orientation) or tall vertical column (horizontal orientation).
- Layers stack with no gap, like geological strata.
- Each layer card has name (large, bold), description (small, muted), and a color.
- Traveler: a packet that descends (encapsulation) or ascends (decapsulation) through the layers.
- Optional: as the packet enters each layer, show the header / footer it adds wrapping around the original data.

## Animation choreography

1. Packet appears at the top (or bottom) layer.
2. Descends into the next layer (250ms slide).
3. The layer "wraps" the packet with its header (small `<rect>` slides in around the existing packet visual).
4. Packet now visually larger (original + header).
5. Repeat until bottom (or top) layer reached.
6. Optionally: reverse and decapsulate going back up.

## Encapsulation visual

```
app data                  ← starts as plain
[header][app data]        ← presentation adds header
[h][h][app data]          ← session adds another
[h][h][h][app data]       ← transport
... and so on
```

Each `[h]` is a small colored `<rect>` matching the layer's color.

## Variants

- **Side-by-side encap + decap** — send on the left, receive on the right; show how each header is added then stripped.
- **OSI vs TCP/IP** — two stacks side-by-side, mapping OSI's 7 to TCP/IP's 4.
- **Memory hierarchy with latency** — each layer labeled with access latency (1ns / 4ns / 12ns / 100ns / ...) so the eye sees the orders of magnitude.

## Pitfalls

1. **Layers as separate cards with gaps** — feels disconnected. Cross-section means literally adjacent.
2. **No headers visualized for encapsulation** — readers don't see what the layer adds. Show the headers wrapping the data.
3. **Layer names in mono uppercase tiny** — they're the most important text in the diagram. Use 16-18px, semibold.
4. **Vertical layout for ≤3 layers** — wasted space, use horizontal.
5. **Both directions at once** — pick send OR receive per play; switching adds confusion.
