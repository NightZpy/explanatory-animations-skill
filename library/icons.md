# Iconography

Three strategies, ask the user during the discovery protocol.

## Strategy A — Emoji (default, fastest)

Universal, zero licensing, scales cleanly, expressive enough for ~80% of explanatory animations.

| Use | Emoji examples |
|---|---|
| Actors | 👤 user · 👥 team · 🤖 bot |
| Servers / services | ☁️ cloud · ⚡ api · 🌐 web · 🎬 worker · 📬 queue |
| Storage | 🐘 postgres · 🔴 redis · 💾 disk · ☁️ object store |
| Tools | 🐙 github · 🔐 secret · 📦 registry · 🛠️ CLI |
| Actions | 📥 download · 📤 upload · 🔔 notify · 📧 email · ✉️ message |
| States | ✅ ok · ⚠️ warn · ❌ failed · ⏳ pending · 🔄 retry |
| Math / science | 📐 angle · 📊 chart · 🧮 math · ⚛️ atom · 🪐 planet · ☀️ sun |
| Mechanical | ⚙️ gear · 🔩 bolt · 🔌 power · 💡 light |
| Geographic | 🌍 globe · 🗺️ map · 🏢 office · 🌐 region |

Render at **24-32px** inside a **40-44px white tile with 1px border**. The tile adds visual weight without making emoji blurry.

```html
<div class="bbg-icon" style="font-size:28px;width:44px;height:44px;
   display:flex;align-items:center;justify-content:center;
   background:#fff;border:1px solid #e7e5e4;border-radius:10px">☁️</div>
```

## Strategy B — Claude finds/draws them

For topics where emoji isn't enough (network protocols, mechanical parts, biology, chemistry, geography), Claude can:

### B.1 — Search Lucide for an icon glyph

Lucide is free, MIT-licensed, has ~1500 line icons. Use for: verbs, abstract concepts (refresh, lock, filter, settings, search, edit).

Inline SVG approach (no dependency):
```html
<svg width="22" height="22" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- paste the body of the lucide icon here -->
</svg>
```

Get the SVG bodies from <https://lucide.dev>.

### B.2 — Draw custom SVG primitives

For things Lucide doesn't have. Stay schematic, never photo-realistic:

- **Server rack**: vertical `<rect>` 40×80 with 3-4 horizontal `<rect>`s inside (the rack units).
- **Database cylinder**: `<ellipse>` on top + `<rect>` body + `<ellipse>` shadow.
- **Gear**: `<circle>` body + 8-12 `<rect>` teeth via rotation, OR a `<path>` with the gear silhouette.
- **Pipe**: `<rect>` with a gradient fill (light at top, dark at bottom for 3D illusion).
- **Planet**: `<circle>` with a `<radialGradient>` for lighting.

Keep stroke widths consistent: 1.5–2px everywhere.

### B.3 — AI image generation (not in this skill)

Avoid generating raster images via DALL-E / SD for explanatory animations. Raster doesn't scale; aesthetic varies; licensing is murky. If the user insists, document the prompt + provider + license in a comment.

## Strategy C — User provides assets

Most flexible. The user pastes URLs or paths to PNG / SVG / WebP files. Ask:

> "Paste asset URLs (one per node), or drop into a folder I can read. For each, tell me what it represents."

Always:
- Verify the asset URL responds 200 before referencing in the animation.
- Specify `width` and `height` on the `<img>` tag so layout doesn't shift.
- Use `alt` text with the role of the asset.
- For raster (PNG/JPG), ask for 2x resolution to support retina displays.
- For SVG, prefer inline (paste the markup) over `<img src>` so the icon inherits color via `currentColor`.

## Decision tree

```
Is the concept clearly emoji-expressible?
├─ yes → Strategy A
└─ no
   ├─ Is it a generic verb / UI concept? → B.1 (Lucide)
   ├─ Is it a domain-specific physical thing? → B.2 (custom SVG primitives)
   └─ Does the user have brand assets? → C (user-provided)
```

## Mistakes to avoid

- **Mixing icon styles** in one animation (some emoji, some Lucide, some custom SVG) — looks inconsistent. Pick one strategy and stick with it. Exception: emoji for actors + Lucide for verbs is OK when clearly partitioned.
- **PNG icon packs** (Material, FontAwesome, etc.) — look like a stock template.
- **Photorealistic illustrations** in a schematic context — break the visual register.
- **Icons that need their own legend** — if a reader doesn't immediately know what the icon means, replace it with a labeled text card.
