# Pattern L — Timeline / sequence

## Use when

- SSL/TLS handshake (client/server back-and-forth with explicit timing)
- OAuth flow (authorize → token → refresh, with redirects)
- Network round-trip diagrams
- Signal timing in electronics (waveforms)
- Project Gantt charts
- Anything where **time itself is the most important axis**

## Don't use when

- The flow is naturally a state machine — use **A** (states have meaning beyond just "happens later")
- Multiple subsystems are key, not the timing — use **B (system flow)**

## Inputs the user must provide

```js
{
  title: "TLS 1.3 handshake",
  lanes: ["Client", "Server"],     // horizontal swim lanes
  totalMs: 4000,                   // total span shown
  events: [
    { atMs: 0,    lane: "Client", to: "Server", label: "ClientHello + KeyShare" },
    { atMs: 800,  lane: "Server", to: "Client", label: "ServerHello + Cert + KeyShare + Finished" },
    { atMs: 1600, lane: "Client", to: "Server", label: "Finished" },
    { atMs: 1900, lane: "Client", to: "Server", label: "HTTP GET /" },
    { atMs: 2700, lane: "Server", to: "Client", label: "200 OK" },
  ],
}
```

## Visual structure

- Horizontal **time axis** along the bottom with tick marks (e.g. every 500ms or 1s).
- Vertical **swim lanes** for each participant.
- Events are arrows between lanes, anchored at their `atMs` x-coordinate.
- A vertical "now" line sweeps from left to right as the animation plays.
- Optional: total elapsed time displayed in the status pill ("elapsed: 2.7s").

## Animation choreography

1. "Now" line starts at t=0, lanes empty.
2. Time line slides right at the configured rate.
3. As "now" reaches each event's `atMs`:
   - The arrow draws from source lane to destination lane (250ms easeOutQuad)
   - The label fades in beside the arrow
   - Optional: a small "ping" pulse at both lane endpoints

## Time scale

```js
const pxPerMs = stage.width / totalMs;
const NOW_X = (currentMs) => currentMs * pxPerMs;
```

The Speed Pill at 1× plays the timeline in real-time (1 ms wall = 1 ms simulated). At 0.5×, slower. At 2×, faster. **For very slow signals** (e.g. an OAuth flow taking 30+ seconds), pre-compress: real 30s → animation 6s, and label both.

## Variants

- **Waveform signal** — replace arrows with square / sine waves running along each lane (good for electronics, sensor timing, audio).
- **Multi-participant** — 3+ lanes, useful for distributed protocols (Paxos, Raft).
- **Annotated phases** — colored background bands showing "ClientHello phase", "Cert phase", etc.
- **Hover an event** to see protocol details — expanded info card with the actual bytes / TLS extensions.

## Pitfalls

1. **No time axis labels** — readers don't know what "halfway through" means. Always label ticks (0s, 1s, 2s, ...).
2. **All events at the same y-coordinate** — readers can't tell who's talking. Use distinct lanes.
3. **Arrow labels overlapping** — when events are close together (<300ms), use staggered y-offsets for labels.
4. **No "now" cursor** — readers can't tell where in time they are when paused.
5. **Hardcoded ms ↔ px scale** — breaks on resize. Compute from current stage width.
