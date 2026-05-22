# Pattern M — Text effects

## Use when

- Social-media reels / short-form video opener
- Big-text reveal for podcast clips, music videos, motion poster
- "Type-in" headline with character stagger
- Word-by-word reveal of a quote or tagline
- Scramble / glitch text for tech / gaming aesthetic
- Magnet / repel interaction on hover (hero sections)
- CTA hooks where text demands the viewer's attention

## Don't use when

- The text is part of an explanation — keep static, animate the diagram instead
- More than 8-10 words at a time — split into chapters / cuts
- Body copy — never animate paragraphs, only headlines and short phrases

## Inputs the user must provide

```js
{
  title: "Make better stuff.",          // the text to animate
  effect: "scramble"                    // M.1 scramble | M.2 split-stagger | M.3 type-on |
                                        // M.4 magnet | M.5 wave | M.6 cascade
                                        // | M.7 reveal-mask
  duration: 1200,                       // total ms for the reveal
  loop: false,                          // loop the effect for video assets
  alternate: false,                     // back-and-forth on loop
  startColor: "#61C3FF",                // optional: from-color
  endColor:   "#ffffff",
}
```

## M.1 — Scramble (glitch in, settle to final)

```js
import { text, animate, createTimeline, stagger } from "https://esm.sh/animejs@4";

const split = text.split('h1', { chars: true });

createTimeline()
  .add(split.chars, {
    opacity: [0, 1],
    duration: 800,
    delay: stagger(20, { from: 'random' }),
    ease: 'inOut(2)',
  })
  .add(split.chars, {
    innerHTML: (el) => [randomGlyph(), randomGlyph(), el.dataset.final],
    duration: 600,
    delay: stagger(15),
    ease: 'steps(20)',
  }, 0);
```

The "scramble" effect cycles through random glyphs before landing on the final character — a tech/cyberpunk staple. Add `' #@$%&*+'.split('')` as the random pool for ascii feel, or japanese/korean codepoints for full anime aesthetic.

## M.2 — Split-stagger (lines/words/chars cascading in)

```js
const split = text.split('p', { lines: true });

createTimeline({
  defaults: { alternate: true, loop: true, loopDelay: 75, duration: 1500, ease: 'inOutQuad' }
})
  .add(split.lines, { color: { from: '#61C3FF' }, y: -10, scale: 1.1 }, stagger(100))
  .add(split.words, { scale: [.98, 1.04] }, stagger(100, { use: 'data-line' }));
```

Use this for **CTAs and big-text reveals** — readers see the whole copy "breathe" line by line. The Anime.js docs page at <https://animejs.com/documentation/text/split> has the canonical example.

`text.split()` config (most useful flags):
- `lines: true` / `words: true` / `chars: true` — pick the unit
- `wrap: 'clip' | 'visible'` — wraps each unit in an overflow box (for slide-in reveal)
- `clone: 'top' | 'right' | 'bottom' | 'left'` — duplicate the text and offset (great for "flip" effects)
- `includeSpaces: true` — animate spaces too (rarely needed)
- `accessible: true` — preserves the original text for screen readers (always on for production)

## M.3 — Type-on (typewriter effect)

```js
const split = text.split('h1', { chars: true });
animate(split.chars, {
  opacity: [0, 1],
  duration: 1,           // instant per-char (no fade, just on/off)
  delay: stagger(50),
});
```

Add a `<span class="cursor">|</span>` after the text that blinks via CSS animation.

## M.4 — Magnet / repel on hover

```js
const split = text.split('h1', { chars: true });
split.chars.forEach(el => {
  el.addEventListener('pointerenter', () => {
    animate(el, {
      x: utils.random(-50, 50),
      y: utils.random(-50, 50),
      duration: 600,
      ease: 'out(3)',
    });
  });
});
// Click anywhere to tidy back
document.addEventListener('click', () => {
  animate(split.chars, { x: 0, y: 0, ease: 'inOutExpo', duration: 800 });
});
```

Used on the Anime.js v4 landing page hero. Great for "explore me" interactive editorials.

## M.5 — Wave (continuous vertical sine)

```js
const split = text.split('h1', { chars: true });
split.chars.forEach((el, i) => {
  animate(el, {
    y: ['0', '-12px', '0'],
    duration: 1500,
    delay: i * 80,
    loop: true,
    ease: 'inOutSine',
  });
});
```

Each character oscillates with a phase offset, creating a sine wave across the text. Good for music / fluid / water topics.

## M.6 — Cascade (slide-in from a direction)

```js
const split = text.split('h1', { words: true, wrap: 'clip' });   // wrap = clip mask
animate(split.words, {
  y: ['100%', '0%'],
  duration: 700,
  delay: stagger(60),
  ease: 'out(3)',
});
```

The `wrap: 'clip'` is the key — it adds an overflow:hidden wrapper around each word, so the slide reveal happens cleanly.

## M.7 — Reveal-mask (text appears as a gradient swipes across)

```html
<style>
  .reveal-mask {
    background: linear-gradient(90deg, transparent 0%, currentColor 30%, currentColor 70%, transparent 100%);
    background-size: 200% 100%;
    background-position: 100% 0;
    -webkit-background-clip: text;
            background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: background-position 1.2s ease;
  }
  .reveal-mask.on { background-position: 0 0; }
</style>
```

Trigger via `.classList.add('on')`. Pure CSS — anime.js not needed. Best for hero "scroll past me" copy with `IntersectionObserver`.

## Variants by aesthetic

| Aesthetic | Effect | Font | Color |
|---|---|---|---|
| **Editorial** (NYT / The Verge) | M.6 cascade | Fraunces | Black on cream |
| **Tech / startup** | M.2 split-stagger | Geist Mono | Voltage yellow on dark |
| **Cyberpunk / gaming** | M.1 scramble | JetBrains Mono | Neon green on black |
| **Music / podcast** | M.5 wave | Space Grotesk | Pastel gradient |
| **Quote / testimonial** | M.6 cascade w/ accent on key word | Editorial serif | Single accent color |
| **CTA / button** | M.4 magnet on hover | Geist | Brand accent |

## Pitfalls specific to M

1. **Animating body paragraphs.** Looks chaotic and hurts reading. Only headlines and short phrases.
2. **No `accessible: true`** in `text.split()` — screen readers see "u s e r f r i e n d l y" character-by-character. Always set `accessible: true`.
3. **Too many chars at high stagger** — the last character takes seconds to start. Cap visible delay at ~800ms total. Use `stagger(n, { from: 'random' })` or `stagger(n, { grid: [w, h] })` to smooth large counts.
4. **Loop on a video export** — you want a finite count, not infinite.
5. **No `font-kerning: none` + `font-variant-ligatures: none`** — letters can fuse weirdly during char-by-char animation. Set both on the container.
6. **Chrome's text rasterization at small sizes** — chars at <14px get blurry on transform. Keep transformed text >18px or use `will-change: transform`.

## Recommended container CSS

```css
.text-fx {
  font-family: 'Geist', sans-serif;
  font-kerning: none;
  font-variant-ligatures: none;
  text-rendering: optimizeSpeed;
}
.text-fx span {
  will-change: color, transform;
}
```

## Reference

Anime.js text splitter docs: <https://animejs.com/documentation/text/split>
