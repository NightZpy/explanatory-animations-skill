---
name: pick-pattern
description: Help the user choose the right animation pattern for what they want to explain. Use when the user asks "which pattern should I use for X?", "what's the best way to visualize Y?", or starts an animation request without committing to a specific pattern yet. Outputs a recommendation + 2-3 alternatives. Does NOT build the widget — hand off to `build-widget` afterwards.
---

This skill runs **only the pattern-selection step** of the 16-pattern catalog. Use it when the user knows the topic but not the pattern.

## How it works

1. Read the user's topic + intent.
2. Open `../animate/patterns/_index.md` to see the 16-pattern catalog.
3. Match against the catalog using the tie-breaker order in `../animate/SKILL.md` § "Pick the pattern (decision tree)".
4. Recommend ONE pattern as the primary pick + 2-3 alternatives, each with a one-line "use this if…" rationale.
5. Hand control back. Do NOT proceed to build the widget here — that's `build-widget`'s job.

## Output shape

```
Pattern recommendation for: <user topic>

Primary pick: <CODE> — <name>
  Why: <one-sentence rationale>

Alternatives:
  · <CODE> — use if <distinguishing condition>
  · <CODE> — use if <distinguishing condition>

To continue:
  - `/explanatory-animations:build-widget <CODE>` to generate the widget, OR
  - Tell me the content / style preferences for the recommended pattern and I'll keep going.
```

## When to defer

If the user is clearly committed to building the animation right away (says "make me an animated X" with concrete details), invoke `animate` instead — that runs the whole flow including this step.

If the user just wants conceptual advice on visualization style without intending to build, this is still the right skill: explain the picks, no widget.

## Referenced files

- `../animate/patterns/_index.md` — full catalog (16 entries) with input requirements per pattern.
- `../animate/SKILL.md` § "Pick the pattern" — tie-breaker order.
- `../animate/patterns/<code>-<name>.md` — read the candidate's doc before recommending, so the rationale is grounded in the pattern's actual "use when" / "don't use when" sections.

## Pitfalls

- **Recommending without reading the pattern's `Don't use when`** section is a common mistake — it's how you suggest Pattern G (orbital) for something that should be Pattern F (mechanical), or vice versa. Always read both `Use when` and `Don't use when` of the top 2 candidates.
- **Three+ alternatives is noise** — the user is choosing, not browsing. One primary + at most three alternatives.
- **Don't list all 16** — picking is the point.
