---
name: ux-walkthrough-report
description: |
  Generate and act on a persona-based UX walkthrough report with dopamine journey tracking.
  Use when: auditing a web app's user experience, identifying friction points, or turning
  UX findings into actionable code fixes. The report format captures an inner monologue
  ("iç ses") from a specific persona, scores each page, tracks a dopamine/engagement
  curve, and produces prioritized action items.
  Example triggers: "UX raporu yaz", "bu rapordaki bulguları düzelt",
  "kullanıcı deneyimini değerlendir", "landing page'i test et", "fix findings from report".
---

# UX Walkthrough Report Workflow

> **Verified**: 2026-02-23 | **Source**: session 199abbea-0b66-4550-a6ba-d063cfca348b

## When to Use

- User provides a UX walkthrough report (markdown) and asks to fix findings
- User asks to evaluate a web app from a first-time visitor's perspective
- Landing page, registration flow, or onboarding needs UX review
- Multiple disconnected UX issues need to be triaged and prioritized

## Report Format

The report follows a consistent structure:

### Persona Definition
```
**Persona:** [age range], [tech level], [attention level], [entry point]
**Pages visited:** N (page1 → page2 → page3)
**Estimated drop-off point:** [page] — [reason]
```

### Per-Page Section
```
## Sayfa N: Page Name (`/path`)

**Iç Ses:** (inner monologue — first-person stream of consciousness as the persona)
> ...
> **(dopamin: X → Y)** [one-line summary of emotional state change]

**Skorlar:**
| Kriter | Skor | Not |
|--------|------|-----|
| Anlasilabilirlik | N/10 | ... |
| Gorsel netlik | N/10 | ... |
| Erisilebilirlik | N/10 | ... |
| Ilk izlenim | N/10 | ... |

**Oneriler:** (numbered list of specific fixes)
```

### Summary Sections
```
## Dopamine Journey
[Landing]  : ██████░░░░ 7 → 6  "reason"
[Register] : ██████░░░░ 6 → 3  "reason"

Peak: [page] (score) — reason
Lowest: [page] (score) — reason
Biggest drop: [page] (X → Y) — reason

## Top 3 Critical Findings
1. **Title** — explanation
2. **Title** — explanation
3. **Title** — explanation

## Average Scores
| Criterion | Avg |
|-----------|-----|

## Priority Actions
1. Most impactful fix
2. Next fix
...
```

## Instructions for Fixing a Report

When given a report file to fix:

1. **Read the report first** — get all priority actions and findings
2. **Read source files in parallel** — fetch all relevant components/pages mentioned in the report simultaneously
3. **Create tasks from priority actions** — one task per finding, using TaskCreate or TodoWrite
4. **Fix them in order of severity** — start with the critical findings
5. **Common fix patterns from UX reports:**
   - Unclickable content → wrap in `<Link to={url}>` (React) or `<a href>` (HTML)
   - Jargon CTA → replace with clear action text ("Enter the Fold" → "Sign Up")
   - Language inconsistency → standardize all user-facing text to one language
   - Low contrast overlay text → increase gradient opacity (`from-black/60` → `from-black/70`), add `drop-shadow-sm`, increase font size
   - Dead-end for unauthenticated users → add guidance text explaining next steps

## Key UX Patterns Discovered

### Landing Page Static Cards Anti-Pattern
A common bug: landing page creates a simplified version of a card component (e.g. `LandingStoryCard`) that strips out all interactivity (no `<Link>`, just `<span>`). The card *looks* clickable but isn't.

**Fix:** Wrap images and usernames in `<Link to={url}>`. Check that the route exists and is public (not behind `ProtectedRoute`).

### Invite-Only Dead End Pattern
Apps with invite-only registration often leave uninvited visitors in a dead end: they reach the register page, find they need a code, and have no path forward.

**Fix:** Add a line: "Don't have a code? Ask an existing member to invite you." near the invitation code field.

### Mixed Language Anti-Pattern
English UI with untranslated labels in one language (e.g., English intro text + Turkish form labels) signals an unfinished product and erodes trust.

**Fix:** Pick one language for all user-facing text. ASCII versions of localized text (e.g., "Kullanici adi" instead of "Kullanıcı adı") are particularly bad — either use proper Unicode or translate everything.

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| N/A — session completed without failures | — | — |

## Common Mistakes

- **Don't**: Only fix the landing page component when a simplified landing variant exists separately
  **Instead**: Search for all card variants (e.g., `LandingStoryCard` vs `StoryCard`) and check if both need the same fix
  **Why**: Landing pages often have stripped-down variants that diverge from the main component

- **Don't**: Assume a route is protected just because similar routes are
  **Instead**: Check `App.tsx` routing — `<Route path="/story/:id">` may be public even if most routes are protected
  **Why**: Knowing whether a route is public determines if linking to it from an anonymous landing page is safe

## See Also

- [Examples](examples.md) - Real examples demonstrating this skill
- [Troubleshooting](troubleshooting.md) - Error → solution mappings

## Version History

- v1.0.0 (2026-02-23): Initial extraction from session 199abbea-0b66-4550-a6ba-d063cfca348b
