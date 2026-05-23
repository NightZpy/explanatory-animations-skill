# 15 common mistakes

These are pattern-agnostic. Pattern-specific pitfalls live in each pattern doc.

1. **Static infographic disguised as animation.** Cards in a row with a dot moving between them is decoration. Real animations have state changes per arrival (highlight, scale pulse, color shift) and the arrow itself lights up as the packet crosses.

2. **Diagonal arrows in an architecture diagram.** ByteByteGo, Stripe Docs, MDN never use diagonals — orthogonal only, even if it takes 3 bends. If the layout requires a diagonal, the layout is wrong.

3. **Edge labels floating without a background.** They overlap the line and become unreadable. Always wrap edge labels in a small `<rect>` matching the paper color, 4 px taller than the text, behind the label.

4. **Numbered steps inside the node cards.** Numbers belong on transitions (arrows), not states (cards). The state machine names the state; the number names the action that took you there.

5. **Auto-play that fires before the widget is visible.** A widget behind a tab or below the fold autoplays + finishes before the reader sees it. Trigger via `IntersectionObserver` at 0.5 threshold + 250 ms layout-settle delay.

6. **Speed control that resets between path changes.** The user sets 2×, switches paths, suddenly back to 1×. Persist `currentSpeed` in a closure outside the timeline factory.

7. **`anime.speed` set after `anime.timeline()` is already running.** The change has no effect on the current run. Always set `window.anime.speed = currentSpeed;` BEFORE `anime.timeline({...})`.

8. **Status indicator that never reaches "done".** The user pauses, scrubs, and the badge still says "playing…". Always emit a terminal state on `timeline.complete`.

9. **No `cursor: not-allowed` + opacity on disabled buttons.** A grayed-out icon button that doesn't change cursor feels broken. Always: `opacity: .45; cursor: not-allowed;`.

10. **Hardcoded pixel coordinates that break on resize.** Compute positions at play time via `getBoundingClientRect`. Debounce resize 200–300 ms, then re-build geometry and re-play from start.

11. **Class reused with `opacity: 0` initial — only animated in some cases.** A shared class like `.token-pill` is used both for animated tokens AND for static raw-string display, but the timeline's selector only animates the token usage. The static instance stays invisible forever. **Fix:** include every usage-class in the animated selector, OR remove the CSS `opacity:0` and use `opacity: [0,1]` inside the animation itself, OR split into two classes (`.token-pill` for animated, `.raw-string` for static).

12. **Pre-setting transforms in CSS for elements Anime.js will animate.** `.card { transform: scale(0.9); }` followed by `animate('.card', { translateY: [6,0] })` makes the card jump to `scale:1` at frame 0 — Anime.js takes over the transform property entirely. **Fix:** never set `transform` in CSS for animated elements; use `utils.set('.card', { translateY: 6, scale: 0.9, opacity: 0 })` before the first animation.

13. **Delay-only `.add()` in v4 — silently does nothing.** Using `tl.add({duration: 1000}, {}, "+=0")` as a "hold" was valid in v3 but in v4 the first argument is treated as a target object and the timeline ends up running ~3× faster than designed. **Fix:** `tl.label("hold-N", "+=1000")` then `.call(cb, "hold-N")`, or push the offset into the next real `.add(target, params, "+=1000")`.

14. **`viz.kind` switch that misses a case.** When the per-step animation branches on `step.viz.kind`, forgetting one kind in the selector leaves that step's visualization frozen at its CSS initial state (e.g. cells stuck at `scaleY: 0.2`). **Fix:** maintain the list of "kinds that use this viz" as an explicit array (`["vectors","qkv","residual"]`) so adding a new kind forces the dev to also list it.

15. **Restart that rebuilds the entire DOM.** Calling `rebuild() + play()` on every Restart click leaks animation instances inside `animate.engine` (their targets are detached but the engine keeps ticking them) and is slow. **Fix:** restart only does `timeline.pause() + timeline.seek(0) + utils.set` to reset child states + `timeline.play()`. Rebuild only when the path actually changes.

## Sanity check before declaring done

Run through the **Output checklist** in [`SKILL.md`](../SKILL.md#output-checklist). If you can't tick every box, the animation is a draft.
