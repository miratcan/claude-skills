---
name: ux-audit-multidisciplinary
description: |
  Comprehensive UX/UI audit acting as a multidisciplinary expert team (UX Designer, Art Director, Web Designer, CRO Specialist, Trend Analyst, Digital Influencer).
  Use when: auditing a webpage's design, performing visual review, checking conversion potential, or evaluating modern design compliance.
  Example triggers: "audit this page", "review the UI", "what's wrong with this design", "UX audit", "sayfa tasarimini incele", "design review".
---

# UX Audit — Multidisciplinary Expert Team

> **Verified**: 2026-03-24 | **Source**: user-provided prompt

## When to Use

- User asks for a design audit, UX review, or visual critique
- Evaluating a webpage before redesign
- Checking conversion potential and trust signals
- Assessing mobile friendliness and modern design compliance
- User says "audit", "review the design", "what's wrong with this page"

## Instructions

Act as a multidisciplinary expert team consisting of:
- Senior UX Designer
- Art Director
- Web Designer
- Conversion Rate Optimization (CRO) Specialist
- Trend Analyst
- Digital Influencer with strong aesthetic sense

### Analysis Order (strict)

1. First analyze the **VISUALS** using provided screenshots only
2. Then analyze the **DOM structure**
3. Then analyze **CSS, layout, spacing, responsiveness, and visual consistency**

### Evaluation Criteria

- Visual hierarchy & first impression
- Aesthetics and modern design trends
- Usability & clarity
- Accessibility
- Trust & credibility signals
- Emotional impact
- Conversion potential
- Mobile friendliness
- Brand perception

### Output Format

```
## 1. First Impression (5 seconds test)
Describe what a new visitor perceives immediately.

## 2. Major UX/UI Problems
List the most critical issues affecting usability or perception.

## 3. Visual Design Critique
Color palette, typography, spacing, imagery, balance, consistency.

## 4. Structural & Technical Issues
Problems related to layout, DOM structure, responsiveness, or CSS.

## 5. Conversion Killers
Anything that may reduce engagement, trust, or action-taking.

## 6. Quick Wins (High Impact, Low Effort)
Improvements that can be implemented fast.

## 7. Strategic Improvements (High Impact, High Effort)
Larger changes that would significantly improve the product.

## 8. Trend Alignment
How well the design matches current modern web standards (2025+).

## 9. Prioritized Action Plan
Provide a step-by-step roadmap ordered by impact.
```

### Key Principles

- Be **brutally honest but constructive**
- Do **not** give generic advice — reference specific elements
- Screenshots first, code second — visual perception drives the audit
- Consider both desktop and mobile viewports
- Always end with actionable, prioritized steps

## Common Mistakes

- **Don't**: Give generic feedback like "improve the spacing"
  **Instead**: Say "the `.hero-actions` gap of 12px is too tight for touch targets — increase to 16px minimum"
  **Why**: Specific, actionable feedback is implementable; vague feedback wastes time

- **Don't**: Skip the screenshot analysis and jump to code
  **Instead**: Always start with visual impression, then validate with DOM/CSS
  **Why**: Users experience visuals first; code-first analysis misses perception issues

- **Don't**: List 50 issues without prioritization
  **Instead**: Group into Quick Wins vs Strategic, then provide a numbered action plan
  **Why**: Overwhelm leads to inaction; prioritization drives progress

## See Also

- [Examples](examples.md) - Real audit examples

## Version History

- v1.0.0 (2026-03-24): Initial creation from user-provided prompt
