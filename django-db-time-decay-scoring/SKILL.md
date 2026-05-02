---
name: django-db-time-decay-scoring
description: |
  Implement Hacker News-style time decay feed ranking in Django ORM using DB-level annotation, cross-compatible with SQLite and PostgreSQL.
  Use when: replacing chronological feed ordering with freshness-weighted scoring, implementing "new content beats old popular content" ranking.
  Formula: score = (likes + comments * weight + featured_boost) / (age_hours + 2)
  Example triggers: "feed ranking with freshness", "time decay score Django ORM", "Hacker News algorithm Django", "new posts beat old popular ones"
---

# Django DB-Level Time Decay Feed Scoring

## When to Use

- Replacing chronological feed (`order_by("-created_at")`) with engagement + freshness scoring
- Implementing Hacker News-style ranking where new content competes with older popular content
- Need for DB-level sorting (no Python-side sorting of full querysets)
- Must work on both SQLite (dev) and PostgreSQL (prod)

## The Formula

```
score = (like_count + comment_count * COMMENT_WEIGHT + featured_boost) / (age_hours + 2)
```

- `age_hours`: hours since `created_at` (NOT `updated_at` — use `created_at` so edits don't inflate score)
- `+ 2` in denominator: prevents division by near-zero for very new content, stabilises first 2 hours
- `comment_count * 2`: comments signal deeper engagement than likes
- `featured_boost`: flat additive boost for curated/featured content

## Implementation

### 1. Settings

```python
# settings.py
FEED_COMMENT_WEIGHT = 2
FEED_FEATURED_BOOST = 10
```

### 2. Cross-DB age helper

```python
from django.db import connection
from django.db.models import ExpressionWrapper, F, FloatField, Func
from django.db.models.functions import Now


class _JulianDayNow(Func):
    """JULIANDAY('now') for SQLite — avoids Django Now() wrapping bug."""
    function = "JULIANDAY"
    template = "JULIANDAY('now')"
    arity = 0


def _age_hours_expr():
    """Hours since created_at, compatible with both PostgreSQL and SQLite."""
    if connection.vendor == "postgresql":
        epoch = Func(
            Now() - F("created_at"),
            function="EXTRACT",
            template="EXTRACT(EPOCH FROM %(expressions)s)",
            output_field=FloatField(),
        )
        return ExpressionWrapper(epoch / 3600.0, output_field=FloatField())
    # SQLite: (julianday('now') - julianday(created_at)) * 24
    return ExpressionWrapper(
        (
            _JulianDayNow()
            - Func(F("created_at"), function="JULIANDAY")
        )
        * 24.0,
        output_field=FloatField(),
    )
```

### 3. QuerySet annotation

```python
from django.conf import settings
from django.db.models import Case, ExpressionWrapper, F, FloatField, Value, When


def feed_for(self, user, listing: str):
    # ... existing filter logic (auth, nsfw, blocks) ...

    comment_w = getattr(settings, "FEED_COMMENT_WEIGHT", 2)
    featured_b = getattr(settings, "FEED_FEATURED_BOOST", 10)

    age_h = _age_hours_expr()

    popularity = (
        F("like_count")
        + F("comment_count") * comment_w
        + Case(
            When(
                is_featured=True,
                then=Value(featured_b),
            ),
            default=Value(0),
            output_field=FloatField(),
        )
    )

    score = ExpressionWrapper(
        popularity / (age_h + Value(2.0)),
        output_field=FloatField(),
    )

    return qs.annotate(feed_score=score).order_by("-feed_score", "-id")
```

## Testing Strategy

Tests must bypass `auto_now_add` to set specific `created_at` values:

```python
def _set_created_at(story, dt) -> None:
    """Bypass auto_now_add to set a specific created_at."""
    Story.objects.filter(pk=story.pk).update(created_at=dt)
    story.refresh_from_db()
```

Key test scenarios:
- New story with few likes beats old story with many likes
- Featured boost works (same age + likes, featured one ranks higher)
- Comment weight works (4 comments beats 4 likes at same age)
- 7-day-old 50-like story ranks below 2-hour-old 2-like story

## Common Mistakes

- **Don't**: Use `updated_at` for age calculation
  **Instead**: Use `created_at`
  **Why**: `updated_at` with `auto_now=True` refreshes on every save, so editing an old post would inflate its freshness score

- **Don't**: Use `Func(Now(), function="JULIANDAY")` on SQLite
  **Instead**: Use a custom `_JulianDayNow` with `template = "JULIANDAY('now')"` and `arity = 0`
  **Why**: Causes `sqlite3.OperationalError: user-defined function raised exception`

- **Don't**: Use Django's `Power()` function for gravity exponent (e.g., `(age+2)^1.5`)
  **Instead**: Use gravity=1 (simple division) or integer gravity with multiplication
  **Why**: Django's `Power()` only works on PostgreSQL; SQLite lacks a `POWER()` function

- **Don't**: Compute scores in Python after fetching the queryset
  **Instead**: Use `annotate()` and let the DB sort
  **Why**: Python-side sorting requires fetching all rows; DB-level is efficient and pageable

## See Also

- [Examples](examples.md) - Complete working implementation
- [Troubleshooting](troubleshooting.md) - SQLite-specific errors
