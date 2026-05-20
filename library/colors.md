# Color palettes

Three presets, plus a strategy for brand-aligned palettes. Pick one with the user during the discovery protocol.

## Preset 1 — Voltage (default)

Best for: technical docs, engineering content, ByteByteGo-style architecture, lifecycle diagrams.

```css
:root {
  --paper:        #fafaf7;   /* canvas */
  --paper-2:      #fdfdfb;   /* slightly raised */
  --card:         #ffffff;   /* node fills */
  --ink:          #09090b;   /* primary text */
  --ink-2:        #3f3f46;
  --ink-3:        #71717a;
  --ink-4:        #a1a1aa;   /* idle borders/lines */
  --border:       #e7e5e4;
  --border-2:     #d4d4d8;

  --accent:       #eab308;   /* "you are here" */
  --accent-bg:    #fef3c7;
  --accent-ink:   #713f12;
  --accent-glow:  rgba(234,179,8,.45);
}
```

## Preset 2 — Editorial

Best for: product/marketing content, story-driven explanations, journalistic context.

```css
:root {
  --paper:        #fdf7ec;   /* warm cream */
  --paper-2:      #fefaf2;
  --card:         #ffffff;
  --ink:          #1c1917;   /* warm black */
  --ink-2:        #44403c;
  --ink-3:        #78716c;
  --ink-4:        #a8a29e;
  --border:       #e7e3dc;
  --border-2:     #d6d3d1;

  --accent:       #c2410c;   /* coral */
  --accent-bg:    #ffedd5;
  --accent-ink:   #7c2d12;
  --accent-glow:  rgba(194,65,12,.40);
}
```

## Preset 3 — Neon dark

Best for: sci-fi topics, security/cryptography, anything where "the system is humming in the dark".

```css
:root {
  --paper:        #0f0f17;   /* near black */
  --paper-2:      #161624;
  --card:         #1f1f33;
  --ink:          #f4f4f5;
  --ink-2:        #d4d4d8;
  --ink-3:        #a1a1aa;
  --ink-4:        #71717a;
  --border:       #2d2d44;
  --border-2:     #3d3d5c;

  --accent:       #22d3ee;   /* electric cyan */
  --accent-bg:    rgba(34,211,238,.15);
  --accent-ink:   #67e8f9;
  --accent-glow:  rgba(34,211,238,.55);

  --accent-2:     #e879f9;   /* magenta secondary */
}
```

## Preset 4 — Brand-aligned (custom)

When the user provides a brand hex:

1. Make their color the `--accent`.
2. Derive `--accent-bg` by mixing with `--paper` at 18% opacity.
3. Derive `--accent-ink` by darkening 30% (mixed with `--ink`).
4. Use the **Voltage** foundation (paper/card/ink/border) as the chrome.

This keeps brand consistency without producing a fully branded animation that looks like marketing.

## Semantic tones (apply per-node by role)

Identical across all 4 presets — these are the "what kind of thing is this" colors. Always pair with a tone-specific border + text.

```
pending  →  bg #f4f4f5  stroke #a1a1aa  ink #3f3f46
warn     →  bg #fff7ed  stroke #d97706  ink #7c2d12
ok       →  bg #dcfce7  stroke #16a34a  ink #14532d
bad      →  bg #fee2e2  stroke #dc2626  ink #7f1d1d
db       →  bg #fce7f3  stroke #be185d  ink #500724
queue    →  bg #fed7aa  stroke #c2410c  ink #7c2d12
external →  bg #ede9fe  stroke #7c3aed  ink #3b0764
edge     →  bg #dbeafe  stroke #2563eb  ink #1e3a8a
```

Adjust for Neon dark: darken backgrounds to ~15% saturation, brighten text to `#f4f4f5`.

## Path colors (multi-flow animations)

When animating concurrent flows, use distinct path colors:

```
amber   #eab308   default async / happy path
blue    #3b82f6   sync request / read path
emerald #10b981   success / commit path
rose    #ec4899   side branch / notification
red     #dc2626   failure / error path
```

**Rule:** never >3 path colors in one animation. If the system needs 4+, split into separate animated views.

## Boundary region backgrounds

Layer boundaries use very low-saturation gradients (~5% alpha) + 1px dashed border tinted to match the layer:

```css
.region-client { background: linear-gradient(180deg, rgba(249,115,22,.05), rgba(249,115,22,.02)); border: 1px dashed rgba(249,115,22,.35); }
.region-app    { background: linear-gradient(180deg, rgba(99,102,241,.05), rgba(99,102,241,.02)); border: 1px dashed rgba(99,102,241,.35); }
.region-data   { background: linear-gradient(180deg, rgba(190,24,93,.05),  rgba(190,24,93,.02)); border: 1px dashed rgba(190,24,93,.35); }
.region-external { background: linear-gradient(180deg, rgba(124,58,237,.05), rgba(124,58,237,.02)); border: 1px dashed rgba(124,58,237,.35); }
```

The `<span class="region-label">` floats top-left with `position: absolute; top: -10px; left: 16px; background: var(--paper); padding: 0 8px;` so it visually "cuts" the dashed border.

## Mistakes to avoid

- Don't use rainbow palettes (>3 path colors).
- Don't pair `--ink` with `--paper` of a different preset (text becomes washy).
- Don't use semantic tones for things that aren't semantic (e.g. don't make "queue" pink just because it looks nice).
- Don't pick branded colors for the chrome — keep brand in the accent only.
