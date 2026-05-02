# UI Mockup in HTML — Examples

## Example 1: peeka.pics Full Redesign

**Source session:** 627dcad1-f6c6-4227-9fc4-b206b213ee43
**Date:** 2026-02-25
**Project:** peeka.pics (resmin2)

### Context
User wanted to explore a warm, intimate visual direction for a pseudonymous photo Q&A app. Figma AI was tried first but produced poor results. The HTML mockup approach was used instead.

### Design Exploration Journey
1. Started with skeuomorphism and jQuery UI nostalgia (rejected — too nostalgic)
2. User shared a design screenshot (Grok-generated retro pixel art) for reference
3. Built `mockup-warm-redesign.html` with 6 screens: Landing, Feed, Story Detail, Hall of Fame, Club Detail, Profile
4. Iterated on: typography (multiple font combos), color palette (burgundy → gray), icon system (emojis → Lucide SVG icons), link styles (underline vs color)

### What Worked
- Phone frames with labels gave user instant app-level perspective
- Changing one CSS variable (font or color) for quick A/B comparisons
- Palette footer documented decisions in-context
- 6 screens in one file meant all app contexts visible at once
- Using Lucide icons via CDN (`<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js">`) removed emoji "unprofessionalism"

### Key CSS Decisions Made via Mockup
```css
:root {
  --cream: #F3EDE4;      /* Background — warm, not white */
  --navy: #283744;       /* Header — dark but not black */
  --accent: #6B6B6B;     /* Neutral gray — "no brand color" */
  --pink: #C15D63;       /* Only for liked/featured states */
  --text-dark: #1A1A1A;
  --text-mid: #5C5C5C;
  --text-light: #9A9A9A;
}
```

### Why This Works
The mockup let user reject wrong directions cheaply. Skeuomorphism test, jQuery UI test, font family comparisons, burgundy→gray color shift — all done in disposable HTML before touching real code. Total mockup iteration time: ~2-3 hours. Real codebase migration: ~4 hours. Ratio is good.

### Applying to Real Code
After mockup was approved, the CSS was **directly copied** into the real codebase's `style.css`. Tailwind was fully removed because the mockup already had a complete design token system. See `tailwind-to-plain-css-migration` for that part.
