# Examples

Real examples from sessions demonstrating this skill. This file grows over time as new sessions contribute examples.

---

## Example: Photo App Landing Page Walkthrough

**Context**: Testing a photo sharing app's landing page from a persona's perspective before launch

### Problem

Needed to evaluate the landing page UX from the perspective of a first-time visitor who arrived via a shared link, has moderate tech experience, and low attention span.

### Solution

**Persona built**:
> 26-35 yaş, moderate tech experience, low attention, first visit. Arrived via a shared link — curious but impatient. Starting dopamine: 7/10.

**Key findings from live walkthrough (Playwright)**:

1. **Story cards not clickable** — The most critical bug discovered: `<article>` tags without `<a>` wrappers. Persona clicked on a photo, nothing happened, and dropped off. This is a real UX bug (not just aesthetic).

2. **Login button low contrast** — Login/register button blended with the header background. Persona almost missed it.

3. **Mixed language labels** — English slogan with Turkish form labels in the register page. Confusing for international users.

4. **Invite-only form** — Register page explains invite-only system in English but persona didn't read past first sentence.

**Inner voice example (Page 1 - Landing)**:
> "A link I clicked opened a page. Dark blue-grey background... app name in the top left, sounds fun. Large slogan in the middle — hmm, English? Photos below. Looks nice. But... what am I supposed to do here? I don't see a button. There's a small 'Login' in the top right but it almost blends in. Let me scroll... more photos. Ok but how do I join? Not clear."

**Dopamine journey**:
- Landing: 7/10 → saw beautiful photos → 8/10
- Clicked photo, nothing happened → 5/10
- Found register form → 4/10 (long form, invite-only confusion)
- Estimated drop-off: Register page

### Why This Works

The combination of:
- `browser_snapshot` revealing `<article>` without `<a>` (non-clickable cards)
- `browser_take_screenshot` showing visual contrast of login button
- Persona's low attention calibration narrating the 3-second scan behavior

...produced actionable bugs that wouldn't surface in a technical code review.

---

## Example: Educational Platform — Child Persona

**Context**: Testing an interactive educational game platform from the perspective of a primary school child

### Problem

Needed to evaluate a Turkish educational game hub from the perspective of a 7-10 year old child with low tech experience, low reading tolerance, and high curiosity/dopamine (school context, purposeful visit).

### Notable: Skill Not Found in Registry

The user first asked "ux walkthrought skilin var mi?" — the `ux-walkthrough` Skill tool call returned `Unknown skill`. The skill existed at `skills/ux-walkthrough/SKILL.md` in the project repo but wasn't registered as a plugin. Claude correctly recovered by reading the SKILL.md file directly with the Read tool and executing it manually.

**Lesson**: A skill file in the project repo is not automatically discoverable via the Skill tool — it must be registered in a plugin. Until then, read it manually with the Read tool.

### Notable: Playwright MCP Chrome Conflict

Mid-walkthrough, `browser_snapshot` failed with `browserType.launchPersistentContext: Failed to launch the browser process`. The screenshot from the previous navigation had already been captured. Fix applied:
```bash
pkill -f "Google Chrome.*mcp-chrome" 2>/dev/null; sleep 1; echo "done"
```
Navigation resumed successfully on the next attempt.

### Persona Built

> 7-10 yaş (ilkokul), tech-averse, low attention span, first visit. Came to school (purposeful, high dopamine start: 8/10). Extra context: using on a touchscreen whiteboard in class.

### Key Findings (partial — session covered landing page)

1. **Game categories immediately visible** — Clear emoji-led headings (➕ Matematik, 🔬 Fen Bilimleri, 🔤 İngilizce) gave a strong first impression. Child persona could identify subject areas without reading.
2. **No login friction** — Direct game access from homepage without registration matched child audience perfectly. Dopamine maintained.
3. **Turkish-only** — Accessibility snapshot confirmed all labels in Turkish. No language confusion for target audience.

### Why This Works

Persona calibrated for low reading tolerance correctly identified emoji/icon scanning as primary navigation mode — which the site supported well. The child persona's low attention with high dopamine (game-motivated) revealed that the site's frictionless entry was its strongest UX asset.

---
