# Pattern G — Orbital / celestial

## Use when

- Solar system (planets around sun, moons around planets)
- Atomic structure (electrons in shells around nucleus)
- Satellite constellations (Iridium, GPS, Starlink)
- Binary stars / gravitational systems
- Planetary gears (a kind of orbit too)

## Don't use when

- Only one body moves — overkill, use **F (mechanical)** with a simple rotation
- The interesting thing is the resulting force / event, not the motion — use a still diagram + annotations

## Inputs the user must provide

```js
{
  title: "Inner solar system",
  viewBox: "0 0 800 800",
  center: { x: 400, y: 400, name: "Sun", icon: "☀️", radius: 30, color: "#fbbf24" },
  bodies: [
    { id: "mercury", name: "Mercury", icon: "🪨", radius: 4,  orbitRadius: 90,  periodMs: 880   },
    { id: "venus",   name: "Venus",   icon: "🟡", radius: 7,  orbitRadius: 130, periodMs: 2240  },
    { id: "earth",   name: "Earth",   icon: "🌍", radius: 8,  orbitRadius: 180, periodMs: 3650  },
    { id: "mars",    name: "Mars",    icon: "🔴", radius: 6,  orbitRadius: 240, periodMs: 6870  },
  ],
  showOrbits: true,    // draw faint circles for the orbital paths
  showLabels: "always" | "on-hover" | "never",
  trail: false,        // draw a fading trail behind each body
}
```

`periodMs` is the time for one full revolution at 1× speed. Use realistic ratios (Earth = 1 year = baseline) but scale so the visualization is watchable (e.g. 3650ms = 3.65s per revolution).

## Visual structure

- SVG canvas, centered on `center.x, center.y`
- Static elements: central body (sun / nucleus / center of mass), faint orbit circles if `showOrbits`
- Animated: each body is a `<g>` containing the body sprite + optional label
- Each `<g>` rotates around the center; the body itself lives at `(orbitRadius, 0)` so the rotation moves it in a circle

## Animation choreography

This is the cleanest looping pattern of all 12 — every body is on `loop: true` with its own period.

1. **Setup** — all bodies positioned at random angles around the center (so they don't start in a line)
2. **Loop** — each body rotates its parent `<g>` element via `rotate(deg)` transform
3. **Speed pill** — multiplies all periods together (0.5× = half speed, 2× = double speed)
4. **Pause** — pauses all anime instances at their current angle
5. **Restart** — resets all bodies to their starting angles

## Anime.js skeleton

```js
bodies.forEach(b => {
  const g = svg.querySelector(`#orbit-${b.id}`);
  // place body at (orbitRadius, 0) inside the g, so rotation moves it in a circle
  g.querySelector(".body").setAttribute("cx", b.orbitRadius);
  g.querySelector(".body").setAttribute("cy", 0);
  // initial angle so bodies aren't aligned
  const startAngle = Math.random() * 360;
  g.style.transformOrigin = `${center.x}px ${center.y}px`;
  g.style.transform = `rotate(${startAngle}deg)`;

  b._anim = anime({
    targets: g,
    rotate: [startAngle, startAngle + 360],
    duration: b.periodMs,
    loop: true,
    easing: "linear",
    autoplay: false,
  });
});

function play()    { bodies.forEach(b => b._anim.play()); }
function pause()   { bodies.forEach(b => b._anim.pause()); }
function restart() { bodies.forEach(b => b._anim.restart()); }
function setSpeed(s) { anime.speed = s; }  // global multiplier
```

## Variants

- **Elliptical orbits** — replace `rotate` with explicit `x` and `y` via a parametric function (`x = a·cos(t), y = b·sin(t)`)
- **Tilted orbits** — wrap the body in two `<g>`s; outer rotates the orbital plane, inner rotates the body around it
- **Trail** — each body has a `<path>` that accumulates the last N positions, opacity fading from 1.0 (head) to 0.0 (tail)
- **Atomic** — replace sun with nucleus, planets with electrons, orbit lines are quantized "shells" (s, p, d), bodies skip to a different shell when "excited" by a click
- **Speed by Kepler's law** — automatically compute periods from orbital radii using `T² ∝ R³`

## Pitfalls specific to G

1. **All bodies starting at angle=0.** They line up like a barcode. Random initial angles.
2. **All periods identical.** Outer planets must move slower (longer period). If unsure, use Kepler's third law: `period ∝ radius^1.5`.
3. **Body rotation conflated with orbit.** Planets also spin on their own axis. If you want to show that, add a second rotation INSIDE the orbital group. Don't replace one with the other.
4. **No labels.** Watching anonymous dots orbit is meditative but not educational. Use `showLabels: "always"` for educational content.
5. **2D-only when topic is genuinely 3D.** Sun + 8 planets in coplanar 2D is fine. Tilted orbits of comets, binary star systems, gravitational lensing — those need a faked-perspective view or a separate "3D" toggle.
