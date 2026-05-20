# Pattern E — Term-by-term math reveal

## Use when

- Deriving an identity (Pythagorean, Euler's formula, completing the square)
- Step-by-step algebraic transform
- Substituting a value into a formula
- Showing the parts of a Bayes / probability expression
- Walking through a proof

## Don't use when

- The topic is about computation, not algebra — use **C (cursor)** instead
- Better explained with a non-math visualization (most "math" topics are clearer with a geometry-driven pattern + an equation underneath)

## Inputs the user must provide

```js
{
  title: "Completing the square",
  steps: [
    { latex: "ax^2 + bx + c = 0",            note: "start with the quadratic" },
    { latex: "x^2 + \\tfrac{b}{a}x + \\tfrac{c}{a} = 0",  note: "divide by a" },
    { latex: "x^2 + \\tfrac{b}{a}x = -\\tfrac{c}{a}",     note: "isolate the x terms" },
    // ...
  ],
  highlight: [
    { stepIdx: 1, range: [4, 9], color: "amber" },  // highlight term "x^2 + b/a x"
    { stepIdx: 2, range: [0, 7], color: "blue"  },
  ],
}
```

LaTeX rendering: use **KaTeX** (faster than MathJax, ~50KB), load from CDN.

## Visual structure

- One line of LaTeX per step, stacked vertically.
- New steps fade in below the previous one (don't replace).
- Highlights are colored underlines or background tint on specific terms.
- Tiny "note" caption next to each step explaining the transformation.

## Animation choreography

1. Step 1 fades in (350ms easeOutQuad).
2. Note appears next to it (200ms).
3. 1.5s pause for reader to absorb.
4. Step 2 fades in below step 1; the related term in step 1 highlights (underline draws across).
5. Repeat.

## Variants

- **Equality bracketing** — when step N transforms expression X, draw a colored bracket connecting the part in step N-1 to the part in step N that it became.
- **Term coloring (3blue1brown style)** — give each variable a persistent color (`x` always blue, `b` always amber) so the eye tracks them across transformations.
- **Substitute & evaluate** — for "plug in numbers", animate the variable disappearing and the value sliding into its place.

## Pitfalls

1. **Replacing the previous step instead of stacking** — readers lose the chain.
2. **Too many steps shown at once** — limit the visible window to e.g. 5 lines; fade older ones above into the top.
3. **No highlights** — math gets harder without knowing which term changed.
4. **Using plain text instead of LaTeX** — `x^2` typed as ascii is ugly; readers parsing math need the typeset version.
5. **Animating during the reveal** — KaTeX render is instant; don't animate the LaTeX itself, only the entry of each step.
