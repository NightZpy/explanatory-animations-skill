# 10 common mistakes

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

## Sanity check before declaring done

Run through the **Output checklist** in [`SKILL.md`](../SKILL.md#output-checklist). If you can't tick every box, the animation is a draft.
