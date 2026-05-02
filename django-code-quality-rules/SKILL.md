---
name: django-code-quality-rules
description: |
  Enforce Django code quality standards: ruff with no inline imports, dead code
  detection, 79 char limit, raw_id_fields in admin, justfile for commands,
  pre-commit hooks with uv. Use when: starting Django project, setting up linting,
  or enforcing code quality rules.
---

# Django Code Quality Rules

## When to Use

- Starting a new Django project
- Setting up linting and pre-commit hooks
- Enforcing code quality standards in an existing project

## Django Backend Rules

### 1. Ruff Configuration

**MUST HAVE** in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 79
target-version = "py311"
extend-exclude = ["**/migrations/*.py"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "DJ",   # flake8-django
]

[tool.ruff.lint.per-file-ignores]
"*/migrations/*" = ["E501", "DJ01"]

[tool.ruff.lint.isort]
known-first-party = ["your_project_name"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]
```

**Critical**: NO inline imports. All imports at module top level.

```python
# WRONG
def my_view(request):
    from django.contrib.auth import authenticate
    user = authenticate(...)

# CORRECT
from django.contrib.auth import authenticate

def my_view(request):
    user = authenticate(...)
```

### 2. Dead Code Detection

```bash
pip install vulture
vulture . --min-confidence 80
```

During code changes, explicitly check and remove:
- Unused imports
- Unused functions/classes
- Commented-out code blocks (delete, don't comment — git history is the backup)
- Unreachable code after returns/raises

### 3. Line Length: 79 Characters

Strict PEP 8 adherence. Use multi-line formatting:

```python
# WRONG
result = some_service.get_data(param1=value1, param2=value2, param3=value3, param4=value4)

# CORRECT
result = some_service.get_data(
    param1=value1,
    param2=value2,
    param3=value3,
    param4=value4,
)
```

For long strings, use implicit concatenation:
```python
message = (
    f"User {user.email} has exceeded their limit of "
    f"{user.plan.query_limit} queries this month"
)
```

### 4. Django Admin: Always Use raw_id_fields

For **ALL** ForeignKey and ManyToManyField in admin:

```python
class ArticleAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content']
    raw_id_fields = ['author', 'tags', 'categories']
```

**Why**: Without `raw_id_fields`, Django loads entire related table into dropdown. With 10k+ records, admin becomes unusable.

### 5. Justfile for Common Commands

```justfile
default:
    @just --list

dev:
    python manage.py runserver 0.0.0.0:8000

migrate:
    python manage.py migrate

makemigrations:
    python manage.py makemigrations

test:
    pytest -v

lint:
    ruff check .

format:
    ruff format .

dead-code:
    vulture . --min-confidence 80

check: lint dead-code
    python manage.py check
    pytest --maxfail=1 -q

shell:
    python manage.py shell_plus

superuser:
    python manage.py createsuperuser
```

### 6. Pre-commit Hooks

#### With uv (recommended)

Add to `pyproject.toml`:
```toml
[dependency-groups]
dev = [
    "ruff>=0.14.3",
    "pre-commit>=4.0",
]
```

Install:
```bash
uv sync --all-groups
uv run pre-commit install
```

**Important**: Run from repo root with `--project` flag:
```bash
uv run --project backend pre-commit run --all-files
```

#### With pip

```bash
pip install pre-commit
pre-commit install
```

#### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.3  # match your pyproject.toml ruff version
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict

  - repo: local
    hooks:
      - id: vulture
        name: vulture (dead code)
        entry: vulture
        language: system
        args: ['.', '--min-confidence', '80']
        pass_filenames: false

      - id: django-check
        name: django check
        entry: python manage.py check
        language: system
        pass_filenames: false
        files: \\.py$
```

If using monorepo (backend/ + frontend/), scope hooks with `files: ^backend/` and add TypeScript check:
```yaml
  - repo: local
    hooks:
      - id: tsc-check
        name: TypeScript check
        entry: bash -c 'cd frontend && npx tsc --noEmit'
        language: system
        files: ^frontend/.*\.ts$
        pass_filenames: false
```

#### ruff format "files were modified" Error

When `ruff format` hook reformats files, the commit fails:
```
ruff format..............................................................Failed
- files were modified by this hook
```

**Solution**: Re-stage and retry:
```bash
git add -u
git commit -m "..."  # second attempt passes
```

### 7. Unit Tests

Write tests for:
- All business logic (services, utilities, helpers)
- Django models (custom methods, properties)
- Views (logic, not just status codes)

Skip tests for:
- External API calls (mock them)
- Django admin auto-generated code
- Migrations

Split fast/slow tests for pre-commit performance:
```
tests/
├── unit/           # Fast, no external deps → pre-commit
└── integration/    # Slow, external APIs → CI only
```

## Vulture False Positives

Create `.vulture_whitelist.py`:
```python
# Django model magic methods
_.objects
_.__str__
_.get_absolute_url
_.save
_.clean

# Django admin
_.list_display
_.list_filter
_.search_fields
_.raw_id_fields
```

Update hook args: `['.', '.vulture_whitelist.py', '--min-confidence', '80']`

## Failed Attempts

| What Was Tried | Why It Failed |
|----------------|---------------|
| Manual linting reminders | Inconsistent. Pre-commit hooks enforce automatically. |
| Allowing inline imports "just this once" | Inconsistency leads to mixed styles. Zero tolerance. |
| Not using raw_id_fields | Admin loads 50k objects into dropdown. Page timeout. |
| Commenting out dead code | Codebase clutter. Git history is the backup. |
| Running full test suite in pre-commit | 30+ second commits. Split into unit/integration. |
| `uv run pre-commit run --all-files` without `--project` | pre-commit can't find repo root. Use `--project backend`. |

## Common Mistakes

- Skipping pre-commit setup thinking "we'll add it later" — set up in first commit
- Using `# noqa` to silence warnings without good reason
- Not excluding migrations from ruff — Django auto-generated migrations hit E501
- `.pre-commit-config.yaml` in wrong directory — must be in repo root (next to `.git`)
- Panicking at "files were modified by this hook" — just re-stage and retry
