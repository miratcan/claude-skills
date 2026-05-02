---
name: mypy-strict-django
description: |
  Fix mypy --strict errors in Django projects with untyped dependencies.
  Use when: encountering "User | AnonymousUser" errors, "import-untyped" warnings,
  or library stub issues with django-allauth, channels, stripe, or similar packages.
  Example triggers: "mypy is failing", "56 mypy errors", "request.user type error",
  "import-untyped", "no attribute on AnonymousUser".
---

# Mypy Strict Mode with Django

> **Verified**: 2026-02-09 | **Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d

## When to Use

- Running `mypy --strict` on a Django + Django REST Framework project
- Encountering "User | AnonymousUser" type union errors in views
- Getting "import-untyped" warnings for third-party Django packages
- Library stub missing errors (django-allauth, channels, stripe, gemini, nanoid, etc.)
- Protocol definition issues with async methods
- Test file type annotation errors

## Instructions

### Step 1: Categorize All Errors

Run mypy and group errors by type:

```bash
mypy . | tee mypy_errors.txt
```

Common categories:
1. `request.user` type union (User | AnonymousUser vs User)
2. Library stubs missing (import-untyped, no-untyped-call)
3. Generic type arguments missing (dict → dict[str, Any])
4. Test client type mismatches
5. Protocol/async method definitions

### Step 2: Fix request.user Type Narrowing

**Problem**: Django returns `User | AnonymousUser`, but DRF views with `@api_view` + `IsAuthenticated` guarantee `User`.

**Solution**: Use `cast()` to narrow the type:

```python
from typing import cast
from django.contrib.auth.models import User

@api_view(["GET"])
def my_view(request: Request) -> Response:
    user = cast(User, request.user)  # Safe because IsAuthenticated
    # Now user is typed as User, not User | AnonymousUser
```

**Where to apply**: Every view function/method that accesses `request.user`.

### Step 3: Configure Per-Module Overrides for Untyped Libraries

Add to `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["mypy_django_plugin.main"]

# Disable import-untyped globally
disable_error_code = ["import-untyped"]

# Per-module overrides for untyped libraries
[[tool.mypy.overrides]]
module = [
    "allauth.*",
    "channels.*",
    "stripe.*",
    "google.generativeai.*",
    "nanoid.*",
    "anthropic.*",
]
ignore_missing_imports = true

# Test files: relax strict rules
[[tool.mypy.overrides]]
module = "tests.*"
disable_error_code = ["no-untyped-def", "no-untyped-call"]
```

**Key insight**: Use `disable_error_code = ["import-untyped"]` globally instead of per-module, then use `ignore_missing_imports = true` for specific problem libraries.

### Step 4: Fix Generic Type Arguments

Replace bare `dict`, `list`, `set` with parameterized versions:

```python
# Before
def handle_webhook(data: dict) -> None:

# After
def handle_webhook(data: dict[str, Any]) -> None:
```

### Step 5: Fix Test Client Types

Django's `TestCase.client` is typed as `Client`, but DRF methods like `force_authenticate` are on `APIClient`.

**Solution**: Explicit type annotation:

```python
from rest_framework.test import APIClient

class MyTestCase(APITestCase):
    client: APIClient  # Override the type

    def setUp(self) -> None:
        self.client = APIClient()  # Now mypy knows it's APIClient
```

### Step 6: Fix Protocol Async Methods

See [python-protocol-async-methods](../python-protocol-async-methods/SKILL.md) skill.

### Step 7: Verify

```bash
mypy .  # Should show: Success: no issues found
```

## Failed Attempts

| What I Tried | Why It Failed | Lesson Learned |
|--------------|---------------|----------------|
| Using `@login_required` decorator to prove `request.user` is User | mypy doesn't understand decorator contracts | Use explicit `cast(User, request.user)` instead |
| Installing type stub packages for allauth/channels | Stubs don't exist or are incomplete | Use per-module overrides in pyproject.toml |
| Adding `type: ignore[import-untyped]` to every import | Creates maintenance burden, clutters code | Use `disable_error_code = ["import-untyped"]` globally in mypy config |
| Making Protocol methods `async def` | mypy error: "Protocol member cannot be async" | Use `def method() -> AsyncIterator` instead |

## Common Mistakes

- **Don't**: Add `# type: ignore` comments everywhere to silence errors
  **Instead**: Fix the root cause with proper configuration and type narrowing
  **Why**: Type ignores defeat the purpose of strict mode and hide real type issues

- **Don't**: Try to add type stubs for every untyped library
  **Instead**: Use per-module overrides to skip libraries without good stubs
  **Why**: Many Django ecosystem packages don't have stubs, and creating them is not worth the effort

- **Don't**: Assume `request.user` is always `User` without casting
  **Instead**: Always cast when you have authentication guarantees
  **Why**: Django's type stubs correctly model the union type, you need to narrow it explicitly

## See Also

- [Examples](examples.md) - Real examples demonstrating this skill
- [Troubleshooting](troubleshooting.md) - Error → solution mappings

## Version History

- v1.0.0 (2026-02-09): Initial extraction from session c83524b7-7c46-4673-a9aa-dd34b7d9f81d
