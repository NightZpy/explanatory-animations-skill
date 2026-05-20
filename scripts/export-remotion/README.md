# Remotion compositions for the explanatory-animations skill

Render the patterns as MP4 via Remotion's React-based pipeline. Use this path when you want:

1. **In-browser preview + Export button** (Remotion Studio gives you both for free).
2. **Server-side / Lambda rendering** at scale (e.g. personalized reels in CI).
3. **Composable building blocks** — each pattern is a React component that other compositions can include.

If you only need a one-shot MP4 from a standalone HTML widget, use [`../export-widget.py`](../export-widget.py) instead — it's simpler (no Node toolchain, no rewrite).

---

## Quick start

```bash
cd scripts/export-remotion
npm install
npm start                 # → Remotion Studio at http://localhost:3000
                          #   has Preview + Render UI built in
```

The Studio opens in your browser:

```
┌──────────────────────────────────────────────────────────┐
│  ▶ Preview        │  Composition: Lifecycle              │
│  ⚙ Props          │  [animation preview canvas]          │
│  ⬇ Render         │                                      │
│  📁 Output        │                                      │
└──────────────────────────────────────────────────────────┘
```

Click **Render** in the sidebar → pick MP4 / GIF / PNG sequence → choose resolution + duration → download.

## CLI render (for CI / scripted exports)

```bash
# Render to MP4
npx remotion render Lifecycle out/lifecycle.mp4

# Render with custom props
npx remotion render Lifecycle out/custom.mp4 \
  --props='{"title":"Order lifecycle","path":["queued","active","completed"]}'

# Vertical (1080×1920) variant
npx remotion render LifecycleVertical out/lifecycle-9-16.mp4

# Pattern M scramble — landscape and vertical
npx remotion render TextScramble         out/scramble.mp4
npx remotion render TextScrambleVertical out/scramble-9-16.mp4
```

## How patterns port from anime.js to Remotion

| anime.js                              | Remotion equivalent                              |
|---------------------------------------|--------------------------------------------------|
| `createTimeline()`                    | derive everything from `useCurrentFrame()`       |
| `.add({ duration: 700 })`             | `hopFrames = (700 / 1000) * fps`                 |
| `delay: 200`                          | offset the start frame of the hop                |
| `ease: "inOutSine"`                   | `Easing.sin` (or `Easing.bezier(...)`)            |
| `anime.engine.speed = 2`              | render at higher fps / shorter duration          |
| `text.split()` + char animate         | iterate over chars + compute glyph per frame     |
| `loop: true`                          | `loopVolumeCurveBehavior` or modulo on the frame |
| `svg.createDrawable` + `draw`         | animate `strokeDashoffset` via `interpolate`     |

The key shift: anime.js builds a timeline imperatively (the dot's path is determined when the timeline is constructed). Remotion is declarative (the dot's position at frame F is a pure function of F + props). Every animation in Remotion must be **deterministic** — given the same frame and props, the output must be identical. This is what enables parallel rendering at scale.

## Bundled compositions

Two patterns ported as of v0.4. The others (B, C, D, E, F, G, H, I, J, K, L, N, O, P) are roadmap items.

| Composition ID         | Pattern | Resolution    |
|------------------------|---------|---------------|
| `Lifecycle`            | A       | 1920×1080     |
| `LifecycleVertical`    | A       | 1080×1920     |
| `TextScramble`         | M       | 1920×1080     |
| `TextScrambleVertical` | M       | 1080×1920     |

## Add a new composition

1. Drop a `<NewPattern>.tsx` in `src/compositions/`. Export the component + a `z.object()` schema + a `defaultProps` object + a `durationInFrames(props, fps)` helper.
2. Register it in `src/Root.tsx` with a `<Composition>` entry.
3. Restart Studio (or rely on hot-reload) and the new comp appears in the sidebar.

Template:

```tsx
// src/compositions/MyPattern.tsx
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { z } from "zod";

export const mySchema = z.object({
  message: z.string(),
});
export type MyProps = z.infer<typeof mySchema>;
export const defaultMy: MyProps = { message: "Hello" };
export function myDuration(props: MyProps, fps: number) { return fps * 4; }   // 4 seconds

export const MyPattern: React.FC<MyProps> = ({ message }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "#fafaf7", color: "#09090b", display: "grid", placeItems: "center" }}>
      <h1 style={{ opacity, fontSize: 120 }}>{message}</h1>
    </AbsoluteFill>
  );
};
```

```tsx
// src/Root.tsx (add)
import { MyPattern, mySchema, defaultMy, myDuration } from "./compositions/MyPattern";

<Composition
  id="MyPattern"
  component={MyPattern}
  durationInFrames={myDuration(defaultMy, 60)}
  fps={60} width={1920} height={1080}
  defaultProps={defaultMy}
  schema={mySchema}
/>
```

## Resolution / aspect ratio

Set per `<Composition>`. Common pairings:

| Use | Resolution    | Notes                                |
|-----|---------------|--------------------------------------|
| YouTube landscape | 1920×1080 | Default                              |
| YouTube 4K        | 3840×2160 | Set `width` and `height`              |
| TikTok / Reels / Shorts | 1080×1920 | Use a dedicated vertical composition |
| Instagram square  | 1080×1080 | Re-author layout for square          |

For vertical variants, register a second `<Composition>` with `width: 1080, height: 1920` and adjust the component layout via the `vertical: true` prop (see `Lifecycle` for the pattern).

## In-browser export workflow (Remotion Studio)

For the "user previews, clicks Export, downloads MP4" UX:

1. Run `npm start`.
2. Open `http://localhost:3000` in the browser.
3. Pick the composition (left sidebar).
4. Tweak props via the Props panel (live preview updates).
5. Click **Render** → choose format, resolution, duration → MP4 lands in `out/`.

The Studio runs locally, but everything happens in the browser — no manual ffmpeg, no Playwright config. This is the cleanest one-button export experience the skill supports.

## Notes & caveats

- Remotion requires Node ≥ 18 and Chrome (it bundles its own Chromium).
- First `npm install` is ~250 MB (Remotion ships Chromium).
- `remotion studio` opens a localhost server — kill with `Ctrl+C`.
- Renders are deterministic: same props + frame → same pixels. Never use `Math.random()` directly in a composition — use `random(seed)` from `remotion`.

## Resources

- Docs: <https://www.remotion.dev/docs>
- Player (embed without Studio): <https://www.remotion.dev/docs/player>
- Lambda (parallel server render): <https://www.remotion.dev/docs/lambda>
- License: free for individuals + small teams, paid for ≥4-person companies. See <https://www.remotion.dev/docs/license>.
