---
name: code-like-djangonaut
description: Provides Django web framework expertise including project structure, models, views, admin, Celery tasks, testing, and Python best practices. Use when generating, analyzing, refactoring, or reviewing Django/Python code.
source: https://github.com/vigo/claude-skills
---

# Django Development Skill

## When to Use

Use this skill when:

- Writing, reviewing, or refactoring Django applications
- Creating or modifying Django models, views, admin, forms
- Setting up Django project structure and tooling
- Implementing Celery tasks and signals
- Writing Django tests
- Configuring linters (ruff, pylint) for Python/Django

## Prerequisites Check

Before starting any Django work:

```bash
python --version
cat .python-version 2>/dev/null
echo $VIRTUAL_ENV
python -c "import django; print(django.VERSION)"
command -v ruff
```

---

## Instructions

### General Coding Approach

- All naming and comments must be in **English**
- Follow Python (PEP 8) and Django conventions
- Virtual environment must be activated
- Detect project's Python version and use appropriate features
- **Do not use type annotations** (Django doesn't fully rely on them)
- If annotations are needed, import: `from __future__ import annotations`

---

### Formatting and Linting

#### Ruff Setup

Minimal `.ruff.toml`:

```toml
line-length = 119
indent-width = 4
target-version = "py312"
exclude = [
    "**/migrations",
    "**/manage.py",
]

[format]
quote-style = "single"
exclude = ["**/manage.py"]

[lint]
select = ["ALL"]
allowed-confusables = ["ı", "'"]
mccabe.max-complexity = 15
ignore = [
    "ANN",    # annotations
    "D",      # docstrings (pydocstyle)
    "D203",   # one-blank-line-before-class
    "D213",   # multi-line-summary-second-line
    "ISC001", # implicit string concat
    "COM812", # missing trailing comma
    "ERA",    # commented out code
    "RUF012", # mutable class default
    "FBT002", # boolean default positional arg
    "TD003",  # missing todo link
    "FIX002", # line contains todo
    "PT009",  # pytest unittest assertion
    "PT019",  # pytest fixture param
    "PT027",  # pytest unittest raises
    "PGH004", # file-wide noqa
    "INP001", # implicit namespace package
]

[lint.flake8-quotes]
inline-quotes = "single"
docstring-quotes = "double"

[lint.pylint]
max-statements = 100
max-returns = 20
max-args = 10
max-positional-args = 8
max-branches = 20

[lint.isort]
known-first-party = ["core"]
section-order = [
    "future",
    "standard-library",
    "django",
    "third-party",
    "first-party",
    "local-folder",
]

[lint.isort.sections]
django = ["django"]
```

#### Acceptable noqa Comments

- `# noqa: S324` - hashlib security
- `# noqa: SLF001` - Model._meta access
- `# noqa: ARG002` - unused args in Django overrides

Always ask before adding other noqa comments.

---

### Coding Style

#### Quote Convention

Always use **single quotes**. Double quotes only for docstrings:

```python
# Good
user_name = 'vigo'
page = request.GET.get('page')

# Acceptable (contains single quote)
message = "vigo's number"
```

#### No Magic Values

```python
USER_MAX_AGE = 10

def check_age(user):
    if user.age > USER_MAX_AGE:
        pass
```

#### Dict Access

Always use `.get()`:

```python
value = FOO.get('bar')
value = FOO.get('bar', 'default')
```

#### Error Handling

Never use blind exceptions. Every service must have its own exception:

```python
class ProjectError(Exception):
    def __init__(self, message, humans=False, **extras):
        if humans:
            message = message.title()
        super().__init__(message)
        self.humans = humans
        self.message = message
        self.extras = extras

class NotificationServiceError(ProjectError):
    ...
```

---

### Django Project Structure

```
core/
    admin/
        __init__.py
        user.py
    fixtures/
    forms/
        __init__.py
        user.py
    management/
        commands/
    migrations/
    models/
        __init__.py
        user.py
    services/
        __init__.py
        notification.py
    signals/
        __init__.py
        user.py
    tasks/
        __init__.py
        notification.py
    templates/
    views/
        __init__.py
        auth/
    checks.py
    storage.py
```

---

### Model Rules

#### Method Order

1. Field declarations
2. Custom managers
3. `class Meta`
4. `__str__`
5. `save`
6. `natural_key`
7. `get_absolute_url`

#### Model Checklist

| Requirement | Example |
|-------------|---------|
| Manager with `get_by_natural_key` | `objects = PostManager()` |
| `class Meta` with required attrs | `app_label`, `db_table`, `verbose_name`, `verbose_name_plural` |
| `natural_key` method | Must match manager's `get_by_natural_key` |
| `verbose_name` on all fields | Use `gettext_lazy`: `verbose_name=_('title')` |
| Choices as callable | `choices=get_language_choices` |
| Relational fields with all kwargs | `to`, `related_name`, `related_query_name`, `on_delete` |

---

### Admin Rules

Admin files live in `<app>/admin/<model>.py`.

Minimum properties:
- `list_display`
- `list_display_links`
- `search_fields`
- `ordering`

For ForeignKey fields, always add:
- `autocomplete_fields`
- `list_select_related`

---

### View Rules

- **Only Class-Based Views** (no function-based views)
- Separate business logic into **service layer**

---

### Internationalization

Never use hardcoded strings. Always use `gettext_lazy` / `gettext`:

```python
from django.utils.translation import gettext_lazy as _
```

---

### Celery Tasks

Tasks live in `<app>/tasks/`. Always use `bind=True`, `max_retries`, `default_retry_delay`.

Register in `AppConfig.ready()`.

---

### Testing

Test naming: `test_<type>_<name>.py`

Use stdlib and Django's test suites (`TestCase`).

---

### Django System Checks

Create `checks.py` for custom checks that validate:
- Required environment variables
- Model field `verbose_name` presence and gettext usage
- `class Meta` completeness

---

## Quick Reference

| Task | Command |
|------|---------|
| Run linter | `ruff check .` |
| Format code | `ruff format .` |
| Run pylint | `pylint config core` |
| Run tests | `python manage.py test` |
| Django check | `python manage.py check` |
| Django check deploy | `python manage.py check --deploy` |
