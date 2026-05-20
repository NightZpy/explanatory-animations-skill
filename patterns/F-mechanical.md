# Pattern F — Mechanical / kinematic

## Use when

- How a 4-stroke engine works (pistons + crankshaft + valves)
- Gear ratios / planetary gears
- Pendulum / harmonic oscillator
- Clock mechanism (escapement + balance wheel)
- Linkages (4-bar, slider-crank)
- Pumps / turbines

## Don't use when

- The machine is just a visual metaphor for a process — use a more honest pattern (B / I)
- Topic is electrical, not mechanical — use **H (particle flow)** for electrons

## Inputs the user must provide

```js
{
  title: "4-stroke engine",
  viewBox: "0 0 600 400",
  // Background scene: simple SVG primitives (no photo realism)
  scene: `<rect x="100" y="50"   width="120" height="200" fill="#fff" stroke="#a1a1aa"/>  /* cylinder */
          <circle cx="160" cy="320" r="40" fill="#fff" stroke="#a1a1aa"/>                  /* crankshaft */`,
  // Animated components — each with a transformation that loops
  components: [
    { id: "piston", selector: "#piston", animate: { translateY: [0, 150, 0], duration: 1200, loop: true, easing: "easeInOutSine" } },
    { id: "crank",  selector: "#crank",  animate: { rotate: "1turn",            duration: 1200, loop: true, easing: "linear" } },
    { id: "rod",    selector: "#rod",    animate: { /* derived */ } },
  ],
  // Labels that appear at specific moments (intake / compression / power / exhaust)
  phases: [
    { atMs: 0,    label: "intake"      },
    { atMs: 300,  label: "compression" },
    { atMs: 600,  label: "power"       },
    { atMs: 900,  label: "exhaust"     },
  ],
}
```

## Visual structure

- A 2D SVG illustrative diagram. Stylized, not photorealistic.
- Static background = walls, anchors, rails, cylinders
- Animated foreground = moving parts (pistons, gears, levers)
- Labels overlay = text that appears next to the part currently doing its phase
- Optional: a small annotated "current phase" pill in the controls area

## Animation choreography

This pattern is **looping**, not linear. The reader is meant to watch one full cycle, pause if curious, resume.

1. **Initial state** — all parts at their cycle origin (0°, t=0)
2. **Loop** — `loop: true` on every component animation, all sharing the same cycle duration
3. **Phase labels** — fade in/out timed to the cycle (e.g. `intake` visible from 0-25% of cycle, fade out, `compression` 25-50%, etc.)
4. **Pause** stops all animations mid-cycle; Restart resets t=0

## Anime.js skeleton

```js
// Each moving part gets its own anime() call with loop:true
const piston = anime({
  targets: "#piston",
  translateY: [0, 100, 0],     // up-down stroke
  duration: cycle,
  loop: true,
  easing: "easeInOutSine",
  autoplay: false,
});

const crank = anime({
  targets: "#crank",
  rotate: 360,
  duration: cycle,
  loop: true,
  easing: "linear",
  autoplay: false,
});

// Sync them with a master controller
function play() { piston.play(); crank.play(); }
function pause() { piston.pause(); crank.pause(); }
function restart() { piston.restart(); crank.restart(); }

// Phase labels via overlay timeline (also looping)
const labels = anime.timeline({ loop: true, autoplay: false });
phases.forEach((p, i) => {
  const next = phases[i + 1]?.atMs || cycle;
  labels.add({ targets: `#phase-${p.label}`, opacity: [0, 1, 1, 0], duration: next - p.atMs, easing: "linear" }, p.atMs);
});
```

## Variants

- **Top-down view** (good for gears, rotors, turbines): rotation-dominant, simpler geometry
- **Cross-section / side view** (good for pistons, cylinders, pumps): translation + rotation combined
- **Schematic** (no physical drawing, just labeled boxes + arrows + cyclic motion arrows): for when the user wants to teach the principle without the diagram
- **Adjustable RPM**: replace `speed` pill with an RPM slider 100-3000 that maps to `cycle = 60000/rpm`

## Pitfalls specific to F

1. **Easing mismatch** — pistons use easeInOutSine (sinusoidal physics), gears use linear (angular velocity is constant). Mixing them looks unphysical.
2. **Components going out of sync after pause/play.** Always pause/play via a master controller, not per-component buttons.
3. **No phase labels.** A piston pumping silently isn't pedagogy — the labels (intake / compression / power / exhaust) are what teaches.
4. **Photo-realistic illustrations.** They look like an asset pack and break the cohesive style. Stay schematic.
5. **Too fast at 1×.** Mechanical patterns benefit from `0.25×` as a default speed option — engines run too fast at real RPM to follow visually.
