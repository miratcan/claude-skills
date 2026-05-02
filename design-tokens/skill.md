---
name: design-tokens
description: Core design token rules shared across all platforms (web, React Native, etc). Load this alongside platform-specific skills. Covers color pairing, opacity ban, and minimal scale.
---

# Design Tokens — Platform-Agnostic Rules

These rules apply regardless of platform. Web uses CSS custom properties, React Native uses TypeScript objects — the underlying principles are the same.

## Rules

### 1. Color Pairs

Every background color MUST have a paired foreground. Name the foreground after the surface it sits on — never use a foreground token on the wrong surface.

```
bg        → on-bg, on-bg-muted
surface   → on-surface, on-surface-muted
primary   → on-primary
```

**Key principle:** The token name tells you where it belongs. `on-surface` can ONLY appear on `surface`. If you need a dimmer variant, create a `-muted` token — never reach for opacity.

### 2. Visual Weight Reflects Importance

Before picking a color, assign the element to an importance group. Elements in the same group get the same visual weight. Groups within a surface, ordered from most to least prominent:

1. **User content** — what the user wrote or created (highest contrast)
2. **User-defined structure** — tags, key:value metadata, categories the user explicitly added (accent color, same weight across the group)
3. **System/contextual** — timestamps, IDs, counts, labels the system generates (muted)

Elements in the same group MUST have the same color weight. Don't use a bright accent for a system-generated ID and a muted tone for a user-defined tag — that inverts meaning.

```
✅ tag: accent color, kv-metadata: same accent color  (both user-defined structure)
✅ entry-id: muted                                     (system-generated, rarely useful)
❌ entry-id: bright yellow, tag: muted                 (inverted importance)
```

### 3. No Opacity for Color Dimming

`opacity` and alpha values (`rgba`, `hsla`) are banned for text and color dimming. Define a `-muted` token instead.

**Why:** Opacity hides contrast ratios from code. Someone has to open a browser to verify readability. A named `-muted` token decides contrast once, at definition time, and guarantees it everywhere.

```
✅ on-bg-muted: "#888"
❌ color: on-bg + opacity: 0.5
```

The only acceptable use of alpha is for non-text effects: `box-shadow`, overlay backdrops, etc.

**Exception — interactive states:** `opacity` is acceptable for disabled, pressed, or loading states on interactive elements (buttons, inputs). These communicate interaction state, not color meaning — the contrast question doesn't apply the same way.

### 3. `md` Anchors to Platform Default

The `md` font size token MUST equal the platform's default body font size — never an arbitrary number.

- React Native: `14` (system default)
- Web CSS: `1rem` (user's browser default)

This makes `md` a meaningful anchor, not a guess. `sm` is smaller than the system default, `lg` and `xl` are larger. If you find yourself writing `fontSize.md + 1` or `fontSize.md - 1`, you're working around the scale — fix the scale or reconsider the design decision.

### 5. Minimal Scale

Define as few spacing and font-size steps as possible. **4 values maximum each.**

A scale with too many steps is as bad as no scale — every component becomes a new decision point and consistency breaks down.

```
spacing: sm, md, lg, xl
fontSize: sm, md, lg, xl
```

**The rule:** When you need a value not in the scale, question the design decision first — not the scale. If after genuine reflection the scale must grow, add one step and document why.

### 6. No Dead Tokens

Every token must be actively used. When you remove a component, remove its tokens. When you add a token, use it immediately.

- No tokens defined "just in case"
- No orphaned tokens after refactors
- Check both directions: adding UI? Add tokens. Removing UI? Remove tokens.

## Quick Reference

| Rule | Do | Don't |
|------|-----|-------|
| Colors | `on-surface` on `surface` | `on-bg` on `surface` |
| Visual weight | user content = bold, system info = muted | system ID in bright accent |
| Same group | tag + kv-metadata → same color weight | tag = accent, kv = muted |
| Muted | define `on-bg-muted` token | `opacity: 0.7` |
| Scale | 4 spacing + 4 font-size max | `xs sm md lg xl xxl xxxl` |
| Dead tokens | remove with component | leave "just in case" |
