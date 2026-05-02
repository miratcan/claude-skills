# Troubleshooting

Error to solution mappings for Django DB-level time decay scoring.

---

## Error: sqlite3.OperationalError: user-defined function raised exception

**Symptom**: All feed-score annotated queries crash on SQLite during tests. The traceback shows the SQL query using `JULIANDAY(STRFTIME(..., 'NOW'))`.

**Cause**: Using `Func(Now(), function="JULIANDAY")` to get current Julian day on SQLite. Django's `Now()` renders to a user-defined `STRFTIME` wrapper that is incompatible as a JULIANDAY argument.

**Solution**: Replace `Func(Now(), function="JULIANDAY")` with a hardcoded template class:

```python
class _JulianDayNow(Func):
    function = "JULIANDAY"
    template = "JULIANDAY('now')"
    arity = 0
```

Use `_JulianDayNow()` with zero arguments in the expression.


---

## Error: Score-based tests pass but score values are wrong (all equal or unexpected order)

**Symptom**: Tests for ordering (e.g., new beats old) fail because stories appear in unexpected order despite the annotation being present.

**Cause**: Often caused by using `updated_at` instead of `created_at` for the age calculation. If `updated_at` has `auto_now=True`, every `.save()` or `.refresh_from_db()` call (including `_set_created_at`) resets `updated_at` to now.

**Solution**: Ensure `_age_hours_expr()` references `F("created_at")`, not `F("updated_at")`.


---

## Error: Tests pass on PostgreSQL CI but fail on SQLite locally (or vice versa)

**Symptom**: The `_age_hours_expr()` function produces correct results on one database but wrong results on another.

**Cause**: The PostgreSQL path uses `EXTRACT(EPOCH ...)` (seconds since epoch / 3600). The SQLite path uses `(julianday('now') - julianday(created_at)) * 24` (Julian day fraction * 24). These are equivalent but each only works on the target DB.

**Solution**: Verify `connection.vendor` branching is correct. Add a quick sanity check in Django shell:
```python
from apps.question.models import _age_hours_expr
from django.db import connection
print(connection.vendor)  # should show "sqlite" or "postgresql"
```


---
