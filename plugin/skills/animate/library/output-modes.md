# Output modes — browser-native vs video-target

Every widget the skill generates falls into one of two output modes. The choice is made in step 5a of the discovery protocol and **determines the layout from the very first line of HTML**. You cannot retrofit one into the other; they have fundamentally different geometric constraints.

## Quick comparison

| Aspect | Browser-native | Video-target |
|---|---|---|
| Primary consumption | Read in a browser tab | Watched as a video file |
| Height | Free / scrolls vertically | Fixed (matches aspect ratio) |
| Width | `min(maxw, 100vw)` | Fixed (matches aspect ratio) |
| Camera | None — the page scrolls | None — the content moves inside the frame |
| Aspect ratio | Whatever fits the content | **Locked**: 16:9, 9:16, or 1:1 |
| Layer reveal | New cards appear *below* previous | Layers expand/collapse *in place* (no scroll) |
| Reading rhythm | Reader paces themselves | Animation paces the viewer |
| Best for | Didactic explanations the user studies | Social media reels, shorts, embedded videos |
| Export to video | ❌ Produces a long thin scrollable WebM, unusable | ✅ Clean, sized correctly |

## Browser-native mode

The natural shape when the user just wants to *understand*. Vertical stack of full-width cards, each card holds one step / layer / state, animation runs inside each card as the reader scrolls (or as the cursor descends).

```
┌─────────────────────────────────────────┐
│  Title                                  │
│  Controls strip (Play/Pause/Restart…)   │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  01  Step name              [tag]       │
│       Description.                      │
│       [in-card visualization]           │
└─────────────────────────────────────────┘
              ↓  connector label
┌─────────────────────────────────────────┐
│  02  Step name              [tag]       │
│       Description.                      │
│       [in-card visualization]           │
└─────────────────────────────────────────┘
              ↓
            (continues — scroll)
```

**Layout rules:**

- Width: `width: min(960px, 100vw - 32px)` centred.
- Height: free. Total page = `sum(card heights) + connectors + header`.
- Each card: padding 28-32 px, generous white space, the in-card viz lives in a fixed area inside the card (e.g. 80-160 px tall depending on viz kind).
- Connectors: small `↓ verbName` labels between cards.
- The "cursor" / focus indicator can be a colored left-border or a small avatar that descends; it does NOT define the frame.
- Controls strip is **sticky** at the top so the user keeps controls while scrolling.

**When to pick this:**

- Default for didactic patterns (A / B / I / K / L) **when the user said "I want to understand X"**.
- Long-form explanations: 8+ steps with prose context per step.
- Reference / docs / tutorial contexts.

**Trade-offs:**

- Cannot be exported to video cleanly — recording captures the scrollable page (long thin frames) or a static viewport (cuts off most steps).
- If the user later wants a video, the widget must be regenerated in video-target mode.

## Video-target mode

The shape when the output will be a video file (reel, short, embedded clip). Everything fits **one frame**, no scroll. Layers expand and collapse *in place*; the camera does not move.

```
16:9  (1920×1080)                          9:16  (1080×1920)
┌─────────────────────────────────────┐    ┌────────────────┐
│ Title         Controls (recording=  │    │   Title        │
│               hidden via ?clean=1)  │    │   ┌──────────┐ │
│ ┌─────────┬───────────────────────┐ │    │   │  Step    │ │
│ │ stack   │   focused step        │ │    │   │  stack   │ │
│ │ overview│   detail + viz        │ │    │   │ (small)  │ │
│ │ (small) │                       │ │    │   └──────────┘ │
│ │         │                       │ │    │   ┌──────────┐ │
│ │         │                       │ │    │   │ focused  │ │
│ └─────────┴───────────────────────┘ │    │   │  step    │ │
│                                     │    │   │  + viz   │ │
└─────────────────────────────────────┘    │   └──────────┘ │
                                           │                │
                                           └────────────────┘
1:1  (1080×1080)
┌─────────────────────┐
│   Step title        │
│  ┌───────────────┐  │
│  │   in-frame    │  │
│  │  viz that     │  │
│  │  morphs from  │  │
│  │  step to step │  │
│  └───────────────┘  │
│   description       │
└─────────────────────┘
```

**Layout rules:**

- Stage element has **fixed width × height** matching the chosen aspect (1920×1080, 1080×1920, 1080×1080). Use `transform: scale(...)` to fit the viewport for preview, but the underlying coordinate system is fixed.
- Inside the stage, content is laid out with `position: absolute` or CSS Grid with explicit row/column sizes — **never** content-defined heights that grow with the data.
- For sequential layers (Pattern I, K, L): use a **focal-vs-overview split** — small map on one side (showing the full stack), large focal area on the other (showing the current step in detail). Or a single focal area where the previous step morphs into the next step in place.
- The "stack overview" sidebar is at most 25-30% of the frame; the rest is the focal area.
- Controls strip lives outside the stage (in an extra row that is hidden by `?clean=1` URL parameter during recording).
- Mark the stage with `data-export-target` so the Export button records only the frame, not the controls.

**When to pick this:**

- Default for content-creator patterns (M / N / O / P) — they are inherently single-frame effects.
- Any time the user says "reel", "short", "video", "post", "share".
- Step counts ≤ 8 (more than that does not breathe in a single frame at video duration ≤ 60s).

**Trade-offs:**

- Less reading detail per step. Long prose paragraphs don't fit; use 1-2 short lines per step.
- Layout is denser and more architecturally constrained. The agent must decide where each region lives upfront.

## Implementation checklist when video-target is chosen

When the user picks video-target in 5a, the widget MUST:

1. **Wrap the visual area in a fixed-size `.stage`**:
   ```html
   <div class="stage" data-export-target style="width: 1920px; height: 1080px; transform: scale(var(--fit)); transform-origin: top left;">
     <!-- everything visible during the recording goes here -->
   </div>
   ```
   And a small script computes `--fit` from `window.innerWidth / 1920` so preview fits the screen without changing the underlying coordinates.

2. **NEVER use vertical scroll inside the stage**. If content overflows the frame, the layout is wrong — re-architect (fewer steps per frame, smaller font, split into overview + focal).

3. **Layers expand and collapse in the same coordinate space**. Don't append new cards below previous ones.

4. **Controls strip is OUTSIDE the stage**, between the stage and the page chrome. The `?clean=1` URL parameter hides it (handled by `library/controls.md` boilerplate).

5. **Aspect-locked CSS variables**:
   ```css
   :root {
     --stage-w: 1920px;
     --stage-h: 1080px;
     /* derived sizes for content live inside the stage scope */
   }
   ```

## Implementation checklist when browser-native is chosen

1. No fixed `.stage` dimensions — let it grow.
2. Sticky controls strip at the top: `position: sticky; top: 0; z-index: 10;`.
3. Cards stack with margin between them; connectors are inline elements between cards.
4. The in-card viz has fixed height but free width (`width: 100%`).
5. If the user later asks "can I export this to video?" — **explain** that this layout would produce an unusable scrollable WebM, and offer to regenerate in video-target mode.

## How the agent decides defaults

If the user did not pick explicitly in 5a, default by:

- **Pattern + verb**:
  - "understand", "explain", "study", "learn", "documentation", "tutorial" → **browser-native**
  - "reel", "short", "video", "post", "share", "social", "youtube", "tiktok", "instagram" → **video-target**
- **Pattern family**:
  - Didactic (A-L) **without** the social/video verbs above → browser-native
  - Content-creator (M-P) → video-target
- When still ambiguous, **ask, don't guess** — getting this wrong wastes the most time of any discovery decision.
