---
name: ui-mockup-in-html
description: Use when the user wants to explore visual design directions, test color palettes, compare layouts, or prototype UI before touching the real codebase. Also use when Figma or other design tools are unavailable or insufficient. Triggers include "mockup", "design test", "try this palette", "how would this look", or any visual exploration before implementation.
---

# UI Mockup in HTML

## Overview

Build self-contained HTML mockup files to explore design directions without touching the real codebase. Faster than Figma, more tangible than describing designs in words, and trivially disposable.

## When to Use

- Exploring a new visual direction (palette, typography, layout)
- Comparing design alternatives side-by-side
- Prototyping a redesign before committing to CSS changes
- User shares design inspiration and wants to see it applied
- Design tool (Figma, etc.) is unavailable or too limited

**When NOT to use:** If the change is small (just swap a color), edit the real CSS directly.

## Core Pattern

### Structure

Single HTML file, no build step, no dependencies beyond CDN fonts. Place in project root as `mockup-{name}.html`.

### Phone Frames for Mobile Apps

Wrap screens in phone-shaped containers for realistic feel:

```css
.phone-frame {
  width: 375px;
  height: 812px;
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}

.phone-grid {
  display: flex;
  gap: 24px;
  padding: 32px;
  flex-wrap: wrap;
  justify-content: center;
}
```

### Multiple Screens Side-by-Side

Show 4-6 key screens in a horizontal grid. Label each with a `.screen-label` positioned above the frame. This gives a full-app overview in one glance.

### Use Real Content

- Pull actual page structure from the codebase (components, routes, data shape)
- Use realistic usernames, question text, timestamps
- Use Unsplash for placeholder photos: `https://images.unsplash.com/photo-ID?w=300&h=300&fit=crop`
- Match the app's real navigation, cards, and layout patterns

### Palette Documentation

Add a footer bar showing the palette values:

```html
<div style="text-align:center; padding:16px; color:#999; font-size:11px;">
  Palette: Cream #F3EDE4 · Navy #283744 · Burgundy #C15D63<br>
  Fonts: Logo Font (logo) · Serif (headings) · Sans (body)
</div>
```

## Quick Reference

| Element | Approach |
|---------|----------|
| Phone frame | 375x812, border-radius 40px, overflow hidden |
| Screen count | 4-6 key screens covers most apps |
| Fonts | Google Fonts via CDN link |
| Photos | Unsplash with size params |
| Interactivity | Minimal — hover states, toggle classes. No JS frameworks. |
| File location | Project root, `mockup-{name}.html` |
| Lifecycle | Disposable. Delete after decisions are made. |

## Process

1. **Read the real codebase first** — understand current components, routes, color variables, layout patterns
2. **Identify the design question** — palette? layout? typography? full redesign?
3. **Build the mockup** — one HTML file, all screens, real content structure
4. **Open in browser** — `open mockup-{name}.html`
5. **Iterate with user** — adjust based on feedback, rebuild fast
6. **Apply to real codebase** — once direction is chosen, update the actual CSS/components

## Applying Mockup CSS to Real Codebase

When the user approves the mockup direction and wants to apply it to the real codebase:

**CRITICAL: Copy the mockup CSS directly. Do NOT translate/convert it.**

The most common failure is trying to "convert" the mockup's plain CSS into the framework the real codebase uses (e.g., Tailwind). This causes:
- Values drifting (exact px values become approximate utility classes)
- Extra mental overhead for every property
- The user having to correct you repeatedly

**The right approach:**
1. Copy the mockup's `:root` CSS variables into the real `style.css` directly
2. Copy the mockup's component class definitions (`.question-section`, `.story-card`, etc.) into real CSS
3. Replace framework class spam in components with mockup class names
4. Only use the framework where you truly need it (not styling)

**If the codebase uses Tailwind:** If the mockup has a complete design token system (CSS variables + component classes), consider fully removing Tailwind — it becomes an unnecessary layer. See `tailwind-to-plain-css-migration` skill.

## Failed Attempts

| What was tried | Why it failed |
|----------------|---------------|
| Converting mockup CSS to Tailwind classes | Values drift, approximate matches, user had to correct Claude multiple times ("bunu Tailwind'e çevirmeye çalışmak yerine direkt kopyalamalıydım") |
| Keeping Tailwind with "minimum integration" after design tokens established | Contradictory systems — user explicitly said "TAILWIND I UZAY BOSLUGUNA GONDERIYORUZ" (we're sending Tailwind to space) |

## Common Mistakes

- **Using lorem ipsum** — kills the feel. Use real content from the app.
- **Building one screen** — show the full flow, at least 4 screens. Context matters.
- **Skipping the codebase read** — mockup should match real app structure, not an idealized version.
- **Over-engineering interactivity** — this is a visual test, not a prototype. Hover states are fine, routing is overkill.
- **Translating CSS to framework classes when applying to real codebase** — copy the mockup CSS as-is, don't convert it.

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-02 | Initial skill |
| 1.1.0 | 2026-02-25 | Added "Applying Mockup CSS" section with critical failure case (Tailwind conversion anti-pattern) |
