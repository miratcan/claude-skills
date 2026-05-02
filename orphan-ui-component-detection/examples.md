# Examples: Orphan UI Component Detection

## Example 1 — GlobalParams BPM Slider (a music app)

**Context**: Implementing a BPM-based beats system. Plan step 7 was "Add BPM Slider — GlobalParams.jsx".
The component was created, the file written, the BPM slider UI implemented correctly.

**Problem**: After running the app and checking the browser, the BPM slider was nowhere visible.
Scrolling through the Settings panel — nothing. Grepping revealed:

```bash
$ grep -r "GlobalParams" src/
src/components/GlobalParams.jsx:export default function GlobalParams(...
```

Only one result — the component's own file. Never imported, never mounted.

**Root cause**: The plan step described creating the file. Wiring it into `Editor.jsx` or `App.jsx`
was a separate implicit step that wasn't done.

**Compounding architecture issue**: Even if it had been imported, the parent component didn't have
an `onUpdateGlobal` callback mechanism — because `sceneState.global` was entirely produced by DSL
code running on the JS side, with no reverse UI→engine update path.

**Solution**: Two options discussed:
1. Import into `Editor.jsx` and implement `onUpdateGlobal` state flow (larger change)
2. Leave as is — BPM is already configurable via DSL `Global({ bpm: 120 })` in scene files

**Why This Works**: Grepping for component name immediately reveals orphan status — zero
additional imports = not mounted = invisible in browser.
