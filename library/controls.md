# Controls strip

Required on every animation widget regardless of pattern.

## Anatomy

```
┌──────────────────────────────────────────────────────────────────────┐
│  ▶ Play   ⏸ Pause   ↻ Restart  │  speed [0.5×] [1×] [2×]            │
│  [path A] [path B] [path C]    │  status: playing… / paused / done  │
└──────────────────────────────────────────────────────────────────────┘
```

Goes ABOVE the animation stage. Don't put it inside the stage — it should always be reachable even when the stage scrolls.

## Components

### Icon buttons (Play / Pause / Restart)

- 30–32 px square, 1 px solid border (`var(--border-2)`), 8 px radius
- Background `var(--card)`, hover `var(--paper)`
- Disabled: opacity 0.45, `cursor: not-allowed`
- Symbols: `▶` `⏸` `↻` (Unicode, no SVG needed)
- Initial state: Play enabled, Pause disabled
- After Play clicked: Play disabled, Pause enabled
- On `complete`: Play enabled, Pause disabled

```css
.sm-icon-btn {
  width: 30px; height: 30px; border-radius: 8px;
  border: 1px solid var(--border-2); background: var(--card);
  color: var(--ink-2); cursor: pointer; font-size: 13px;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all 120ms; padding: 0; line-height: 1;
}
.sm-icon-btn:hover { background: var(--paper); color: var(--ink); border-color: var(--ink-4); }
.sm-icon-btn:disabled { opacity: .45; cursor: not-allowed; }
```

### Speed pill

Segmented control: `0.5× / 1× / 2×`. Active state filled `var(--accent)`, white text.

```html
<div class="sm-speed-pill">
  <button data-speed="0.5">0.5×</button>
  <button data-speed="1" class="active">1×</button>
  <button data-speed="2">2×</button>
</div>
```

```css
.sm-speed-pill { display: inline-flex; background: var(--card); border: 1px solid var(--border-2); border-radius: 8px; padding: 2px; }
.sm-speed-pill button { font-family: var(--font-mono); font-size: 11px; padding: 4px 9px; border: 0; background: transparent; color: var(--ink-2); cursor: pointer; border-radius: 5px; line-height: 1; }
.sm-speed-pill button.active { background: var(--accent); color: #fff; font-weight: 600; }
```

The active button drives `window.anime.speed = parseFloat(button.dataset.speed)`. Must persist across path changes — store `currentSpeed` outside the timeline factory.

For mechanical / orbital patterns, optionally extend to `0.25× / 0.5× / 1× / 2×` since those benefit from slower playback.

### Path selector pill

Only shown if the pattern's underlying flow has multiple paths. Same shape as speed pill but with named labels.

```html
<div class="sm-paths">
  <button class="sm-btn" data-path="happy">Happy path</button>
  <button class="sm-btn" data-path="failure">Failure</button>
</div>
```

```css
.sm-btn { background: var(--card); border: 1px solid var(--border-2); color: var(--ink-2); font-family: var(--font-mono); font-size: 12px; padding: 5px 11px; border-radius: 999px; cursor: pointer; transition: all 120ms; }
.sm-btn:hover { background: var(--paper); border-color: var(--ink-4); }
.sm-btn.active { background: var(--accent-bg); border-color: var(--accent); color: var(--accent-ink); }
```

Selecting a path: pauses current timeline (if any), then plays the new path from start.

### Status indicator

Right-aligned text, mono, 11 px. Reaches a terminal state.

```css
.sm-status { font-family: var(--font-mono); font-size: 11px; color: var(--ink-4); margin-left: auto; }
.sm-status.playing { color: #16a34a; }   /* green */
.sm-status.paused  { color: #d97706; }   /* amber */
```

States: `ready` → `playing…` → `paused` (optional) → `done`.

### Optional: step-through mode

For patterns where the reader benefits from manual stepping (algorithms, math, handshakes), add two extra buttons:

```
↻ Restart   |⏮ Prev   ▶ Play   ⏭ Next|   speed [...]
```

Prev / Next step the timeline by one logical beat. Disable Play while in step-through.

### Optional: annotation toggle

For patterns with hover-tooltips on nodes / edges, add a toggle:

```html
<button class="sm-btn" data-toggle="annotations">ⓘ Annotations</button>
```

Off by default to avoid clutter; user enables when they want to dig deeper.

## Required layout

```html
<div class="sm-controls">
  <div class="sm-paths"> ... </div>      <!-- left -->
  <span class="sm-divider"></span>
  <button class="sm-icon-btn">▶</button>
  <button class="sm-icon-btn">⏸</button>
  <button class="sm-icon-btn">↻</button>
  <span class="sm-divider"></span>
  <span class="sm-speed">speed
    <div class="sm-speed-pill">...</div>
  </span>
  <span class="sm-status">ready</span>    <!-- right, margin-left:auto -->
</div>
```

```css
.sm-controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding: 10px 14px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; margin-bottom: 18px; }
.sm-divider  { width: 1px; height: 20px; background: var(--border); }
```

## Keyboard

Recommended for accessibility:
- `Space` — play/pause
- `R` — restart
- `→` / `←` — next/prev step (if step-through mode)
- `1` / `2` / `3` — switch between paths

```js
document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "INPUT") return; // don't hijack inputs
  if (e.code === "Space") { e.preventDefault(); togglePlayPause(); }
  if (e.key === "r" || e.key === "R") restart();
  if (e.key === "ArrowRight") nextStep();
  if (e.key === "ArrowLeft")  prevStep();
});
```

## Mistakes to avoid

1. **Speed control that resets when picking a new path** — persist `currentSpeed`.
2. **Status never reaching "done"** — always emit on `timeline.complete`.
3. **Pause button enabled when nothing's playing** — wrong state, looks broken.
4. **Auto-play before the widget is visible** — defer to `IntersectionObserver` if behind the fold.
5. **Restart resetting `currentSpeed` to 1×** — leave it where the user put it.
