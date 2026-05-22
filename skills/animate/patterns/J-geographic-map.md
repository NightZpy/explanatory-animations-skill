# Pattern J — Geographic map

## Use when

- Request flow across regions (e.g. CDN edge → origin)
- Supply chain: factory → ship → warehouse → store
- Migration / commute patterns
- Network outages spreading
- Marker constellations (Starlink satellites, undersea cables)

## Don't use when

- Geography is incidental, not essential — use **B (system flow)** with location as a label
- The map is too big / too small for the screen — break into regional sub-maps

## Inputs the user must provide

```js
{
  title: "Multi-region request",
  basemap: "/path/to/world.svg",       // SVG with country paths
  projection: "natural-earth",         // or "mercator" / "equirectangular"
  points: [
    { id: "frankfurt", lat: 50.11, lng: 8.68,    name: "DE — Frankfurt" },
    { id: "nyc",       lat: 40.71, lng: -74.01,  name: "US — New York" },
    { id: "tokyo",     lat: 35.68, lng: 139.69,  name: "JP — Tokyo" },
  ],
  flows: [
    { from: "nyc", to: "frankfurt", via: "great-circle", label: "primary route" },
    { from: "frankfurt", to: "tokyo", via: "great-circle", label: "failover" },
  ],
}
```

## Visual structure

- SVG world map as static background (countries in `var(--ink-4)` faint stroke).
- Points: small filled circles at each lat/lng. Tooltip-on-hover for the name.
- Flows: SVG `<path>` along the great-circle arc (computed from lat/lng pair).
- Animated packet: `<circle>` walks the path via anime's `motionPath`.

## Animation choreography

1. Map drawn static.
2. Source point pulses.
3. Packet travels along the great-circle arc to the destination, 1.5s at 1× (longer than a system-flow segment — distance is part of the story).
4. Destination point pulses on arrival.
5. Optional: a "return packet" travels back if showing round-trip.

## Lat/lng → SVG coordinates

Use a projection library or hand-rolled equirectangular for simple maps:

```js
function project(lat, lng) {
  // For equirectangular projection on a viewBox 1000×500 covering -180..180, -90..90:
  return {
    x: (lng + 180) / 360 * 1000,
    y: (90 - lat) / 180 * 500,
  };
}
```

For Natural Earth / Mercator / orthographic, use D3-geo:
```html
<script src="https://d3js.org/d3-geo.v3.min.js"></script>
<script>
  const projection = d3.geoNaturalEarth1().scale(180).translate([500, 250]);
  const [x, y] = projection([lng, lat]);
</script>
```

## Great-circle arc as SVG path

The shortest path on a sphere between two points is not a straight line in projection. Use d3-geo:

```js
const geoLine = d3.geoPath(projection)({
  type: "LineString",
  coordinates: [[from.lng, from.lat], [to.lng, to.lat]],
});
// returns an SVG "d" attribute
```

## Variants

- **Heat overlay** — fade in colored regions to show "users impacted".
- **Many concurrent flows** — multiple packets on multiple arcs simultaneously, staggered.
- **Zoomable** — wrap in a `<g transform="...">` and let the user pan/zoom via wheel + drag.
- **Timezone-aware** — show local time at each point, ticks forward as the animation plays.

## Pitfalls

1. **Mercator at high latitudes** — Greenland looks bigger than Africa. Use Natural Earth or equal-area.
2. **Straight lines between lat/lngs** — those aren't realistic flight paths. Use great-circle arcs.
3. **No labels on points** — readers don't know what city / region without them.
4. **Loading a 5 MB SVG for the basemap** — pre-simplify with tools like `mapshaper` to <300 KB.
5. **Animating the basemap** — it's the static background. Only points and flows move.
