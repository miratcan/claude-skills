# Examples

## Example: Full Django Project Quality Setup

### Problem

Django project had no automated quality checks. Inline imports scattered throughout, dead code accumulating, admin pages timing out on large tables.

### Solution

**1. pyproject.toml** with ruff (79 char, no inline imports, isort) + vulture for dead code.

**2. Django Admin** with `raw_id_fields` on all FK/M2M fields:
```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']
```

**3. Pre-commit** with ruff + vulture + django check + fast pytest.

**4. Justfile** encoding common workflows (`just dev`, `just check`, `just lint`).

### Result

Automated enforcement — no manual reminders needed. Hooks catch violations before code enters repo.
