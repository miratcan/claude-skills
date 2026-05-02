# Troubleshooting

## Ruff Check Fails on Import Order

**Symptom**: `I001 Import block is un-sorted or un-formatted`

**Solution**: `ruff check --fix .` or configure editor auto-sort on save.

---

## Vulture Reports False Positives

**Symptom**: Django model methods (`__str__`, managers) flagged as unused.

**Solution**: Create `.vulture_whitelist.py` with Django magic methods and update hook args.

---

## Pre-commit Hook Too Slow (>30 seconds)

**Symptom**: `git commit` takes 30+ seconds.

**Solution**: Only run unit tests in pre-commit, integration tests in CI:
```yaml
- id: pytest-fast
  args: ['tests/unit/', '--maxfail=1', '-q']
```

---

## Django Admin Timeout with Large FK Dropdown

**Symptom**: Admin page loads 60+ seconds editing model with FK to large table.

**Solution**: `raw_id_fields` or `autocomplete_fields` (requires `search_fields` on related admin).

---

## ruff format "files were modified by this hook"

**Symptom**: Commit fails after ruff format reformats files.

**Solution**: `git add -u && git commit -m "..."` — hook already fixed the files, just re-stage.

---

## uv + pre-commit: Can't Find Repo Root

**Symptom**: `pre-commit run --all-files` fails from backend/ subdirectory.

**Solution**: Run from repo root: `uv run --project backend pre-commit run --all-files`
