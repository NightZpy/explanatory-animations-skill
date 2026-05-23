# Typography

Pick one pairing during the discovery protocol. Never use Inter, Roboto, Arial, or system-ui as the primary face — they read as "generic AI dashboard".

## Pairing 1 — Geist + Geist Mono (default)

Modern, neutral, distinguishes itself from Inter without being loud. Designed by Vercel.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Geist', system-ui, sans-serif; }
code, .mono { font-family: 'Geist Mono', monospace; }
```

## Pairing 2 — Fraunces + JetBrains Mono

Editorial / story-driven feel. Fraunces is an expressive variable serif; JetBrains Mono is the technical voice underneath.

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Fraunces', Georgia, serif; }
h1, h2 { font-feature-settings: "ss01" on, "ss02" on; letter-spacing: -0.02em; }
code, .mono { font-family: 'JetBrains Mono', monospace; }
```

## Pairing 3 — Space Grotesk + IBM Plex Mono

Startup / technical aesthetic. Space Grotesk has more personality than Inter without being weird.

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Space Grotesk', system-ui, sans-serif; }
code, .mono { font-family: 'IBM Plex Mono', monospace; }
```

## Role → size/weight mapping (same for all pairings)

| Role | Size | Weight |
|---|---|---|
| Node names (inside cards) | 13–14 px | 600 |
| Meta / subtitle / desc | 11–12 px | 400 |
| Code / IDs / paths / status pills | 10–12 px | 500–700 (mono) |
| Step numbers in badges | 11–12 px | 700 (mono) |
| Edge labels (HTTPS, REST, queue.add) | 10–11 px | 500 (mono) |
| Section heading inside widget | 13–15 px | 600 |
| Title pill ("ANIMATION") | 10 px | 700 uppercase (mono) |

## Why mono for labels

Code, identifiers, file paths, protocol names, step numbers, and status text **always** use monospace, regardless of pairing. The mono face is non-negotiable for these — never substitute a proportional font for monospace data. Use whichever mono comes with your chosen pairing.

## Loading strategy

- Use `<link rel="preconnect">` to fonts.googleapis.com + fonts.gstatic.com (with `crossorigin` on the latter).
- Use `display=swap` in the URL so text remains visible during font load.
- Load all needed weights in a single CSS request, not multiple `<link>` tags.

## Fallbacks

Always include a system fallback for resilience:

```css
font-family: 'Geist', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
font-family: 'Geist Mono', ui-monospace, SFMono-Regular, monospace;
```

## When the host page already uses a distinctive font

If the page already loaded another distinctive face (e.g. the Scenorai infra docs use Fraunces editorial), use that for body text and keep **the mono face for code/labels**. Never substitute mono with proportional.
