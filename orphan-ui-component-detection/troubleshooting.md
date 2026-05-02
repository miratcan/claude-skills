# Troubleshooting: Orphan UI Component Detection

## Symptom: UI feature not visible in browser after implementation

**Error message**: (none — React silently skips unmounted components)

**Symptom**: New UI panel / slider / control doesn't appear in the running app.

**Cause**: Component file was created but never imported and mounted in a parent component.

**Solution**:
```bash
# 1. Grep for component name across the codebase
grep -r "ComponentName" src/

# 2. If only one result (the component file itself) — it's an orphan
# 3. Find the correct parent and add:
import ComponentName from './ComponentName';

# 4. Add to parent's JSX render
```


---

## Symptom: Component is imported but still not visible

**Symptom**: `grep` shows an import, but UI is still missing.

**Cause options**:
1. Component is imported but conditionally rendered (`{condition && <Component />}`) and condition is false
2. Component is rendered but positioned off-screen or zero-opacity
3. Component needs required props that aren't passed (renders null internally)
4. Component is rendered inside a container that is itself hidden/collapsed

**Solution**:
```bash
# Find where it's used in JSX
grep -r "<ComponentName" src/

# Check if it's inside a conditional
grep -B5 -A5 "<ComponentName" src/Parent.jsx
```

---

## Symptom: Component was created as part of a multi-step plan but never connected

**Symptom**: Plan had steps like "Create X component" + "Add X to UI" but only the first was done.

**Cause**: Plan steps for file creation vs. wiring are often listed separately. When implementing,
the "create" step marks done, "wire" step gets skipped.

**Solution**: When closing a plan task that involves UI, explicitly verify:
- [ ] File created
- [ ] Imported in parent
- [ ] Mounted in JSX with correct props
- [ ] Visible in browser

