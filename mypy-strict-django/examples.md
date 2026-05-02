# Examples

Real examples from sessions demonstrating this skill. This file grows over time as new sessions contribute examples.

---

## Example: Fixing 56 mypy errors in Django + Channels project

**Context**: A Django + Django Channels + DRF project with mypy --strict enabled. After implementing all features, `mypy .` showed 56 errors across 21 files.

### Problem

Categories of errors:
- 17 errors: `request.user` type union (User | AnonymousUser vs User)
- 8 errors: LLM provider types (anthropic, gemini untyped libraries)
- 3 errors: Library stubs missing (nanoid, channels, allauth)
- 3 errors: Incorrect/unnecessary `type: ignore` comments
- Multiple errors: Generic type arguments missing (dict → dict[str, Any])

### Solution

**1. pyproject.toml configuration:**

```toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["mypy_django_plugin.main"]
disable_error_code = ["import-untyped"]

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

[[tool.mypy.overrides]]
module = "tests.*"
disable_error_code = ["no-untyped-def", "no-untyped-call"]
```

**2. View files (apps/*/views.py):**

```python
from typing import cast
from django.contrib.auth.models import User

@api_view(["POST"])
def create_share(request: Request) -> Response:
    user = cast(User, request.user)  # Added to all 6+ view functions
    # ... rest of view
```

**3. Test files:**

```python
from rest_framework.test import APIClient, APITestCase

class PortfolioViewsTestCase(APITestCase):
    client: APIClient  # Explicit type annotation

    def setUp(self) -> None:
        self.client = APIClient()
        # ...
```

**4. Service files with dict parameters:**

```python
# Before
def handle_webhook_event(self, payload: bytes, sig_header: str) -> str:
    data: dict = event["data"]["object"]

# After
def handle_webhook_event(self, payload: bytes, sig_header: str) -> str:
    data: dict[str, Any] = event["data"]["object"]
```

**5. Admin files (apps/*/admin.py):**

Added `# type: ignore[type-arg, no-any-return]` to ModelAdmin classes since Django admin internals use `Any` extensively and fixing them isn't worth it.

### Why This Works

- **Global disable_error_code**: Prevents "import-untyped" noise from propagating
- **Per-module overrides**: Targets specific problematic libraries without global type checking compromise
- **cast(User, request.user)**: Explicitly tells mypy what DRF's authentication guarantees
- **Test file overrides**: Tests often mock/patch objects in ways that strict mypy dislikes
- **Selective type: ignore**: Used only where fixing would require changes to third-party code

**Result**: 56 errors → 0 errors, full mypy --strict compliance.

---
