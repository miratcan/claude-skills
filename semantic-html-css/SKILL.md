---
name: semantic-html-css
description: Use when building web pages, writing HTML/CSS, creating UI components, styling elements, or setting up a new frontend project. Covers CSS custom properties, semantic markup, wrapper patterns, and reusable layouts.
---

# Semantic HTML & CSS

**First, load and apply [design-tokens](../design-tokens/skill.md) — color pairs, opacity ban, minimal scale, and no dead tokens all live there.**

This skill covers web-specific implementation on top of those shared rules.

## Rules

### 1. CSS Custom Properties for All Values

Every color, size, spacing, and font value MUST be defined as a custom property under `:root`. No raw values in selectors.

```css
/* ✅ Correct */
:root {
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --font-md: 1rem;
}

p { margin-bottom: var(--spacing-sm); }

/* ❌ Wrong — raw values in selectors */
p { margin-bottom: 8px; }
```

Color pairs from `design-tokens` map to CSS custom properties:

```css
:root {
  --color-bg: #1a1a1a;
  --color-on-bg: #e8e8e8;
  --color-on-bg-muted: #888;

  --color-surface: #2a2a2a;
  --color-on-surface: #e0e0e0;

  --color-primary: #00bcd4;
  --color-on-primary: #1a1a1a;
}
```

### 2. Semantic HTML Elements

Use elements for their meaning, not their appearance. Every element should render correctly with zero classes.

```html
<!-- ✅ Correct -->
<button>Save</button>
<nav>...</nav>
<article>...</article>

<!-- ❌ Wrong -->
<a class="button">Save</a>
<div class="nav">...</div>
```

**Key principle:** Style the element, not the class.

```css
/* ✅ Correct */
button {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary);
  color: var(--color-on-primary);
}

/* ❌ Wrong — element needs a class to look right */
.btn { padding: 8px 16px; }
```

### 3. Wrapper Pattern

The wrapper goes INSIDE semantic elements, not outside them.

```html
<!-- ✅ Correct -->
<header>
  <div class="wrapper">...</div>
</header>

<!-- ❌ Wrong -->
<div class="wrapper">
  <header>...</header>
</div>
```

**Why:** Semantic elements often need full-width backgrounds or borders. Wrapper outside breaks that.

### 4. Reusable Layout Patterns

Name layout classes by structure, not by page.

```html
<!-- ✅ Correct -->
<div class="layout-sidebar">...</div>

<!-- ❌ Wrong -->
<div class="profile-page-left-panel">...</div>
```

### 5. Scope Semantic Element Selectors

`<footer>`, `<header>`, `<nav>` can appear in multiple contexts. Never style them unscoped.

```css
/* ✅ Correct */
body > footer { padding: var(--spacing-xl) 0; }
.card footer { padding: var(--spacing-sm); }

/* ❌ Wrong — hits every footer on the page */
footer { padding: var(--spacing-xl) 0; }
```

### 6. No Dead CSS

Every CSS rule must be actively used. When HTML changes, CSS changes in the same commit.

- No unused `:root` tokens
- No orphaned selectors after HTML removal

## Quick Reference

| Rule | Do | Don't |
|------|-----|-------|
| Values | `var(--spacing-sm)` | `8px` |
| Elements | `<button>` | `<a class="button">` |
| Styling | `button { ... }` | `.btn { ... }` |
| Wrapper | Inside `<header>` | Outside `<header>` |
| Layouts | `.layout-sidebar` | `.profile-page-left` |
| Scoping | `body > footer` | `footer { }` |
| Dead CSS | Remove with HTML | Leave "just in case" |

## Common Mistakes

- **Raw values in selectors** — even a one-off `border-radius: 4px` needs a token
- **`<div>` for everything** — check if `<section>`, `<article>`, `<nav>`, `<aside>` fits
- **Wrapper outside semantic elements** — always wrapper INSIDE
- **Page-specific layout classes** — abstract shared layouts
- **Unscoped semantic selectors** — `footer { }` bleeds into card footers, section footers

## Tooling

```bash
npm install --save-dev stylelint
npx stylelint "**/*.css"
```

| Stylelint Rule | What it catches |
|---|---|
| `semantic/no-raw-values` | Raw `#hex`, `px`, `rem` outside `:root` |
| `semantic/no-opacity-dimming` | `opacity` and `rgba()`/`hsla()` alpha |
| `semantic/no-unused-tokens` | Tokens defined but never used |
| `semantic/color-pair-match` | Mismatched foreground/background tokens |
