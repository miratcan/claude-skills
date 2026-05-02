---
name: Orphan UI Component Detection
description: |
  Detect React/JS components that are built but never imported or rendered anywhere in the app.
  Use when: a UI feature is implemented but doesn't appear in the browser, a component was
  written as part of a plan but is missing from the running app, or after a feature implementation
  you test in browser and the new UI is nowhere visible.
  Example triggers: "BPM slider doesn't show up", "I implemented the component but can't find it",
  "the UI is not visible", component built but browser shows nothing changed.
importance: high
version: 1.0.0
---

# Orphan UI Component Detection

## When to Use

- A UI component was implemented as part of a plan step but doesn't appear in the browser
- You added a new settings panel, slider, or control — but testing shows nothing
- A component exists in the codebase but nothing renders it
- "GlobalParams bileşeni hiçbir yerde kullanılmıyor" type discovery

## The Problem

When implementing a feature plan step-by-step, it's easy to:
1. Create the component file ✅
2. Write the component correctly ✅
3. **Forget to import and mount it in the parent** ❌

The component silently exists but is never rendered. No error is thrown.

## Detection Approach

Before declaring a UI feature done, verify the component is actually mounted:

```bash
# Find all usages of the component
grep -r "GlobalParams" src/
grep -r "ComponentName" src/ --include="*.jsx" --include="*.tsx" --include="*.js"
```

If the only result is the component's own file — it's an orphan.

### Checklist Before "Done"

1. **grep for import**: Is the component imported anywhere?
2. **grep for JSX usage**: Is `<ComponentName` appearing in any render?
3. **Check App.jsx / layout files**: Top-level components are usually wired in root/layout
4. **Check the parent file the plan mentioned**: The plan step might reference where it should go

## The Fix

Find the correct parent component and add the import + JSX:

```jsx
// In the parent (e.g., Editor.jsx, App.jsx, Settings.jsx)
import GlobalParams from './GlobalParams';

// In the render/return:
<GlobalParams global={sceneState.global} onUpdateGlobal={handleUpdateGlobal} />
```

## Architecture Caveat

Sometimes a component is intentionally un-mounted because the architecture doesn't support it yet.

In this session: `GlobalParams` was built to show BPM slider, but `sceneState.global` was entirely
driven by DSL code — there was no way to pass UI-driven updates back to the engine. The component
needed a **prop contract** that didn't exist (`onUpdateGlobal`).

**Before mounting an orphan component, check:**
- Does the parent have the required props to pass?
- Is there a state update mechanism for the data it needs to modify?
- Is this a genuine "missing import" bug, or an "architecture not ready" situation?

## Failed Attempts

| What Was Tried | Why It Failed | Lesson |
|----------------|---------------|--------|
| Implemented `GlobalParams` component with BPM slider | Component was never imported in `Editor.jsx` or `App.jsx` | Grep for component name before closing task as done |
| Scrolled around the browser UI looking for BPM slider | It was never rendered, not hidden behind scroll | Missing import = zero DOM presence, not hidden element |
| Assumed plan step "Add BPM Slider — GlobalParams.jsx" meant it was wired | Plan steps describe creating the file, not necessarily wiring it | Always verify: create + import + mount are three separate steps |

## Common Mistakes

1. **Plan says "create GlobalParams.jsx"** — this doesn't mean "wire it into the app"
2. **Component file exists in correct folder** — doesn't mean it's imported
3. **No error thrown** — React won't complain if you never use a component
4. **Build passes** — unused components don't cause build errors (only TypeScript with `noUnusedLocals`)

