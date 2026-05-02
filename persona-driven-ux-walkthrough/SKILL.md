---
name: persona-driven-ux-walkthrough
description: |
  Design and implement a Claude Code skill that simulates a user persona browsing a live website via Playwright and reports chain-of-thought inner voice, UX scores, and recommendations.
  Use when: user asks to create a "UX walkthrough agent", "persona simulation skill", "simulate a user visiting the site", "test UI from user perspective", "predictive user behaviour for UX".
  Example triggers: "bir kullanici personasini alip sayfada gezdirmek istiyorum", "persona gözünden walkthrough", "ux test skill", "simulate user browsing", "user behaviour agent for landing page".
---

# Persona-Driven UX Walkthrough Skill

## When to Use

- User wants to test a web UI from a real user's perspective (not a technical audit)
- Building a skill/agent that browses a live site with Playwright and generates chain-of-thought output
- Designing a "persona simulation" feature for UX research
- User asks for "predictive user behaviour" in the context of UI/UX (not analytics/churn prediction)

## Critical Disambiguation: "Predictive User Behaviour" ≠ Analytics

**Common misunderstanding**: "Predictive user behaviour agent" sounds like churn prediction, engagement analytics, or ML-based recommendations.

**What users often actually want**: A UX simulation skill that:
1. Defines a user persona (age, tech experience, attention level)
2. Browses a live site via Playwright
3. Generates chain-of-thought "inner voice" output from that persona's perspective
4. Reports UX scores + recommendations

**Before assuming analytics**: Ask what the agent is _doing_. If the answer involves "going to a page and narrating what the user sees/feels", it's a persona simulation, not analytics.

## Skill Architecture

### Single-Pass Skill (recommended starting point)

```
/ux-walkthrough <url>
```

1. **Persona creation** (interactive AskUserQuestion):
   - Age range (18-25 / 26-35 / 36-50 / 50+)
   - Tech experience (tech-native / moderate / tech-averse)
   - Attention level (high / medium / low)
   - Platform familiarity (first visit / heard of it / returning)
   - Arrival context (how they got here: social link, Google, friend?)
   - Optional: extra context

2. **Live browse**: Playwright navigates to URL, captures screenshot + accessibility snapshot per page

3. **Per-page report**:
   - Inner voice (chain-of-thought narrative)
   - Scores (comprehensibility, visual clarity, accessibility, first impression — each 1-10)
   - UX recommendations

4. **Summary report**:
   - Top 3 critical findings
   - Estimated drop-off page + reason
   - Score averages
   - Priority action list

### Playwright Tools Used

```
browser_navigate       — open URL
browser_snapshot       — accessibility + DOM structure (aria labels, button text, etc.)
browser_take_screenshot — visual analysis
browser_click          — persona clicks on elements
browser_press_key      — scroll, tab navigation
```

## Mental Model Calibration

The persona's inner voice should be calibrated by parameters:

| Parameter       | Low                              | Medium                         | High                            |
|----------------|----------------------------------|--------------------------------|---------------------------------|
| Tech experience | "What is this? Where do I click?" | "This looks like a login button" | "JWT auth, Bearer token header" |
| Attention span  | 3 sec — if missed, gone          | Scans page, looks for interest  | Reads every element             |
| Reading tolerance | Max 5 words                   | Headline + first sentence       | Reads everything                |
| Error tolerance | Leaves on first confusion        | Tries once more                 | Debugs it                       |

### Dopamine Tracking (dynamic, not static)

Dopamine level changes **page by page**, not set once:
- **Increases**: Beautiful visuals, sense of progress, clear CTAs
- **Decreases**: Long forms, confusing labels, broken interactions, language mismatches
- **Arrival context** sets initial dopamine: came from Instagram link → high curiosity; found via Google → neutral

### Page Navigation Limit

Based on attention level:
- Low: 3-4 pages
- Medium: 5-6 pages
- High: 8-10 pages

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| Assuming "predictive user behaviour" = churn prediction/ML analytics | User meant persona-based UX simulation, not backend analytics | Ask "what does the agent _do_ — does it visit a page and narrate?" before assuming analytics |
| Treating dopamine as a static persona parameter | Dopamine changes with each page interaction, not set once at start | Model dopamine as a running value that updates per page, not a fixed attribute |
| Skipping accessibility snapshot, using only screenshot | Screenshot shows visuals but not aria labels, contrast info, or focusable elements | Always combine screenshot (visual) + accessibility snapshot (structural) for complete analysis |
| Having agent jump to multiple parallel pages | Persona consistency breaks — each agent plays persona slightly differently | For persona simulation, use sequential single-agent approach, not parallel subagents |

## Common Mistakes

- **Don't**: Build complex multi-agent pipeline immediately
  **Instead**: Start with single-pass skill (one skill file, sequential pages)
  **Why**: Simpler to maintain, persona consistency preserved, context window manageable for typical 3-6 page flows

- **Don't**: Use static dopamine/mood level in persona
  **Instead**: Track dopamine as a running state that changes with each page event
  **Why**: Real user engagement is dynamic — beautiful gallery raises it, confusing form drops it

- **Don't**: Only screenshot for analysis
  **Instead**: Also take accessibility snapshot for DOM structure, aria labels, button targets
  **Why**: Snapshot reveals non-visual UX issues (missing labels, tiny touch targets, contrast ratios)

- **Don't**: Hard-code credentials in skill
  **Instead**: Ask for credentials at skill start (optional), skip auth-gated pages if not provided
  **Why**: Skills should be usable without exposing secrets in the skill file

## Output Format

### Per-Page

```
### Page: <Name> (<url>)

**Inner Voice:**
> [Chain-of-thought narrative from persona perspective...]

**Scores:**
| Criterion           | Score | Note |
|--------------------|-------|------|
| Comprehensibility  | X/10  | ...  |
| Visual clarity     | X/10  | ...  |
| Accessibility      | X/10  | ...  |
| First impression   | X/10  | ...  |

**Dopamine state:** [rising/neutral/falling] (X/10)

**Recommendations:**
- [Specific fix]
```

### Summary

```
## Summary

**Persona**: [brief description]
**Estimated drop-off**: [Page X, reason]
**Score averages**: Comprehensibility X | Clarity X | Accessibility X

### Top 3 Findings
1. [Critical issue]
2. [Critical issue]
3. [Critical issue]

### Priority Actions
- [Actionable fix with page reference]
```

## See Also

- [Examples](examples.md) — Real walkthrough examples
- [Troubleshooting](troubleshooting.md) — Playwright interaction issues discovered

