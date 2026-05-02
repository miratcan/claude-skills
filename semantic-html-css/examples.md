# Examples

Real examples from sessions demonstrating this skill.

---

## Example: Directory App Inline Style Extraction

**Context**: Extracting ~136 inline styles from Django templates into CSS classes

### Key Observations

The codebase had:
- Color pairs partially defined (--color-on-bg, --color-surface, etc.) but used inconsistently
- Some inline styles used tokens correctly (`var(--space-4)`) but as inline styles instead of classes
- Mismatched color pairs: `--color-on-bg-muted` used on `--color-surface` backgrounds (violates Rule 2)
- `rgba()` used in `.detail-cover` gradient — acceptable per Rule 2 exception for non-text effects
- Unscoped `footer` selector risk — item cards have `<footer>` that could clash with site `<footer>`

### Lesson

When extracting inline styles to CSS classes, check for:
1. Duplicate class names in existing CSS (caused breakage in first attempt)
2. Color pair mismatches that inline styles were hiding
3. Unscoped semantic element selectors that could bleed across contexts

---
