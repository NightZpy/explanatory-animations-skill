# Pattern catalog — overview

Twelve patterns, each tuned for a class of explanatory animation. Pick the one whose "Use when" matches the topic; deep-dive in the linked doc.

| Code | Name | Use when | Inputs needed | Anime.js features used |
|---|---|---|---|---|
| **A** | Lifecycle / state machine | An entity progressing through states with branches | List of states + edges + paths | `timeline`, multi-segment line walks |
| **B** | System flow | A request travelling through layered architecture | Nodes per layer + edges with sides + path sequences | `timeline`, motion along SVG path |
| **C** | Cursor over data structure | An algorithm acting on a visible structure | Array/tree/hash + ordered list of operations | `keyframes`, `stagger`, transform animations |
| **D** | Side-by-side comparison | Two approaches contrasted | Same two scenes + metric to surface | `timeline` master with synced children |
| **E** | Term-by-term math reveal | A formula or identity derived stepwise | List of terms + equality steps + colors per group | Opacity + transform + `stagger` |
| **F** | Mechanical / kinematic | Physical machine: motor, gears, pendulum | Component diagram + angular velocities + linkages | `loop:true`, infinite rotation, easing variants |
| **G** | Orbital / celestial | Bodies in orbit: solar system, atoms | Orbit radii + periods (Kepler) + body sizes | `loop:true`, sine motion, multi-target stagger |
| **H** | Particle flow | Many entities flowing along paths: data, water, traffic | Source / sink pairs + paths + density | `stagger` with offset, `motionPath`, infinite loop |
| **I** | Layered transformation | Data transformed through stacked layers: LLM, neural net | Input shape + layer specs + transform per layer | `keyframes`, opacity + transform sequences |
| **J** | Geographic map | Flows on a real-world map: regions, supply chain | Map (SVG) + endpoints in lat/lng + flow density | `motionPath` along great-circle arcs |
| **K** | Cross-section / stack | Literal stacked layers: OSI, memory hierarchy | Layers in order + headers/footers + traversal | Slide reveals, opacity, scale |
| **L** | Timeline / sequence | Time-axis explanations: SSL handshake, signal timing | Events on a time line + duration per event | `timeline` keyed to real seconds |

## Cross-pattern rules

All 12 patterns share the same:
- **Controls strip** (Play / Pause / Restart / Speed / Path / Status) — see [`library/controls.md`](../library/controls.md)
- **Palette / typography / icons** — see [`library/`](../library/)
- **Timing reference** — see [`library/timing.md`](../library/timing.md)
- **Accessibility minimum** — `prefers-reduced-motion`, keyboard nav, focus rings

What differs **per pattern**: the geometry, the data shape the user provides, and the anime.js features used.

## How to read a pattern doc

Each `patterns/X-<name>.md` has the same sections:

1. **Use when** — three concrete topics that fit this pattern
2. **Don't use when** — the closest miss patterns (so you don't pick wrong)
3. **Inputs the user must provide** — the minimum data shape
4. **Visual structure** — layout, what's on screen
5. **Animation choreography** — order of events, timing
6. **Anime.js skeleton** — copy-paste starting code
7. **Variants** — common deviations (e.g. mechanical can be 2D top-down or side cross-section)
8. **Pitfalls specific to this pattern** — beyond the general "10 common mistakes"

## Picking when in doubt

If a topic spans multiple patterns, prefer (in this order):

1. **L (timeline)** if time is the most important axis
2. **A (lifecycle)** if states with branches dominate
3. **B (system flow)** if multiple subsystems are involved
4. **I (layered transform)** if the data shape changes per layer
5. **K (cross-section)** if there's a literal physical stack
6. **F (mechanical)** if the topic is a physical machine
7. **G (orbital)** if bodies move in cycles
8. **H (particle flow)** if many similar entities flow
9. **J (map)** if geography is essential
10. **C (algorithm)** if the data structure is the protagonist
11. **D (comparison)** if the punch line is "X beats Y"
12. **E (math)** as a last resort — most math topics are clearer with a *different* pattern + an equation underneath
