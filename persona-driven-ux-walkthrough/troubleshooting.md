# Troubleshooting

Error → solution mappings for quick reference. This file grows over time as new error cases are discovered.

---

## Issue: Story cards / content items appear but are not clickable

**Symptom**: `browser_click` on a story card or content item doesn't navigate anywhere. Page stays the same.

**Cause**: `<article>` or `<div>` elements are styled to look clickable but lack `<a>` wrapper or `onClick` handler. Accessibility snapshot will show no `link` role on the element.

**How to detect**: Check accessibility snapshot — if the element is `article` with no child `link` role, it's not navigable. Also check if cursor changes to pointer on hover.

**What it means for UX**: This is a real bug, not just a simulation artifact. The persona behavior (clicks and nothing happens → drops off) is accurate.

**Solution for skill**: Report this as a critical UX issue. The persona should narrate "I clicked the photo, nothing happened" and this triggers a drop-off / score penalty.


---

## Issue: Skill can't be tested in the same session it was designed in

**Symptom**: After writing the skill file, you try to invoke `/ux-walkthrough` but it's not recognized.

**Cause**: Claude Code needs to restart (or reload plugins) to pick up newly created skill files. Skills are loaded at session start.

**Solution**: After writing the skill, start a new session. Then invoke `/ux-walkthrough <url>` as a real command. In the current session, you can only simulate the skill manually.


---

## Issue: Playwright MCP fails mid-session — "Failed to launch the browser process"

**Symptom**: `browser_navigate`, `browser_snapshot`, or `browser_take_screenshot` returns:
```
Error: browserType.launchPersistentContext: Failed to launch the browser process.
[pid=XXXXX][out] Opening in existing browser session.
[pid=XXXXX] <process did exit: exitCode=0, signal=null>
```

**Cause**: Chrome was already opened (by a previous Playwright action or by the user manually) and the MCP server tries to launch a new persistent context with `--user-data-dir=.../mcp-chrome-XXXXX`. Chrome detects an existing session on that profile and exits immediately instead of opening a new debugging instance.

**Solution**: Kill the stale Chrome process and retry:
```bash
pkill -f "Google Chrome.*mcp-chrome" 2>/dev/null; sleep 1; echo "done"
```
Then retry the original Playwright tool call — it will work on the next attempt.

**Note**: This error is intermittent. It happens when Playwright MCP was used earlier in the session (or in a prior session) and Chrome didn't clean up its profile lock. The fix is reliable.


---

## Issue: Persona misclassified as analytics/ML agent from vague description

**Symptom**: User says "I want a predictive user behaviour agent" and Claude starts designing churn prediction, engagement scoring, or ML pipeline.

**Cause**: "Predictive user behaviour" is ambiguous — it maps to both analytics (ML/backend) and UX simulation (persona/frontend).

**Diagnosis question**: Ask "does this agent visit a page and narrate what a user sees?" If yes → persona simulation. If no → analytics.

**Solution**: Clarify before designing. The UX simulation meaning is actually the more common intent when the user is talking about "going to the landing page" or "seeing what users experience."


---
