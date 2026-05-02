# Troubleshooting

Error → solution mappings for quick reference. This file grows over time as new error cases are discovered.

---

## Error: Argument 1 has incompatible type "User | AnonymousUser"; expected "User"

**Symptom**: Mypy error when passing `request.user` to a function expecting `User`.

```python
def get_portfolio(user: User) -> dict:
    ...

# In view:
portfolio = get_portfolio(request.user)  # Error here
```

**Cause**: Django's type stubs correctly model `request.user` as `User | AnonymousUser` union. Mypy doesn't know that DRF's `IsAuthenticated` permission class guarantees the user is authenticated.

**Solution**:

```python
from typing import cast
from django.contrib.auth.models import User

@api_view(["GET"])
def my_view(request: Request) -> Response:
    user = cast(User, request.user)
    portfolio = get_portfolio(user)  # No error
```

**Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d (2026-02-09)

---

## Error: Library stubs not installed for "allauth" / "channels" / "stripe"

**Symptom**: Mypy warnings about missing stubs:

```
apps/users/models.py: note: Library stubs not installed for "allauth.account.models"
```

**Cause**: Many Django ecosystem packages don't provide type stubs, and community stubs (`types-*` packages) don't exist or are incomplete.

**Solution**: Add per-module overrides in `pyproject.toml`:

```toml
[[tool.mypy.overrides]]
module = [
    "allauth.*",
    "channels.*",
    "stripe.*",
]
ignore_missing_imports = true
```

Also, disable the "import-untyped" error globally:

```toml
[tool.mypy]
disable_error_code = ["import-untyped"]
```

**Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d (2026-02-09)

---

## Error: "Client" has no attribute "force_authenticate"

**Symptom**: In test files using Django REST Framework's test client:

```python
class MyTestCase(APITestCase):
    def test_something(self):
        self.client.force_authenticate(user=self.user)  # Error: Client has no force_authenticate
```

**Cause**: Django's `TestCase` base class types `self.client` as `django.test.Client`, but DRF's `APITestCase` actually provides `APIClient`. Mypy uses the base class type.

**Solution**: Add explicit type annotation:

```python
from rest_framework.test import APIClient, APITestCase

class MyTestCase(APITestCase):
    client: APIClient  # Override the type annotation

    def setUp(self) -> None:
        self.client = APIClient()
        # Now mypy knows it's APIClient
```

**Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d (2026-02-09)

---

## Error: Missing type parameters for generic type "dict" / "list"

**Symptom**: Mypy strict mode requires generic types to be parameterized:

```
services/subscription.py:42: error: Missing type parameters for generic type "dict"
```

**Cause**: `mypy --strict` enables `disallow_any_generics`, which requires `dict`, `list`, `set` to specify their element types.

**Solution**: Add type parameters:

```python
# Before
def handle_event(data: dict) -> None:

# After
from typing import Any
def handle_event(data: dict[str, Any]) -> None:
```

For deeply nested structures where you don't care about precise types, `dict[str, Any]` is acceptable.

**Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d (2026-02-09)

---

## Error: Protocol member cannot be defined via assignment / Protocol member cannot be async

**Symptom**: When defining a Protocol with async methods:

```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    async def stream(self, prompt: str) -> AsyncIterator[str]:  # Error
        ...
```

**Cause**: Protocol methods cannot be declared as `async def` in Python's type system.

**Solution**: Use a regular `def` that returns an async type:

```python
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    def stream(self, prompt: str) -> AsyncIterator[str]:  # Regular def
        ...

# Implementation can be async generator:
class MyProvider:
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        yield "chunk"
```

**Source**: session c83524b7-7c46-4673-a9aa-dd34b7d9f81d (2026-02-09)

---

<!--
To add a new error case, copy the template above and fill in the placeholders.
Include exact error messages when possible - this helps with discoverability.
-->
