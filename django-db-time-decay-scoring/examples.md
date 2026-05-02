# Examples

Real examples from sessions demonstrating Django DB-level time decay scoring.

---

## Example: Story Feed Score-Based Ranking

**Context**: Replacing a chronological story feed (`-updated_at, -id`) with Hacker News-style scoring on a Django Q&A platform. Issue: old popular stories permanently dominated the top of feed.

### Problem

Existing `StoryQuerySet.feed_for()` used `order_by("-updated_at", "-id")`. Old popular stories stayed at top indefinitely. New stories were buried.

### Solution

Complete implementation in `apps/question/models.py`:

```python
from django.db import connection
from django.db.models import (
    Case,
    ExpressionWrapper,
    F,
    FloatField,
    Func,
    Value,
    When,
)
from django.db.models.functions import Now


class _JulianDayNow(Func):
    """JULIANDAY('now') — SQLite-only, avoids Django Now() wrapping."""

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


class StoryQuerySet(models.QuerySet):
    def feed_for(self, user, listing: str):
        # ... existing filter logic unchanged ...

        comment_w = getattr(settings, "FEED_COMMENT_WEIGHT", 2)
        featured_b = getattr(settings, "FEED_FEATURED_BOOST", 10)

        age_h = _age_hours_expr()

        popularity = (
            F("like_count")
            + F("comment_count") * comment_w
            + Case(
                When(is_featured=True, then=Value(featured_b)),
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

Settings added to `config/settings.py`:

```python
# Feed algorithm
FEED_COMMENT_WEIGHT = 2
FEED_FEATURED_BOOST = 10
```

### Test File

`tests/test_question__feed_algorithm.py` — key helper for overriding `auto_now_add`:

```python
def _set_created_at(story: Story, dt) -> None:
    """Bypass auto_now_add to set a specific created_at."""
    Story.objects.filter(pk=story.pk).update(created_at=dt)
    story.refresh_from_db()


def _feed_ids(user=None, listing="public") -> list[int]:
    return list(
        Story.objects.feed_for(user, listing).values_list("id", flat=True)
    )


@pytest.mark.django_db
def test_new_story_beats_old_popular(user_factory, story_factory):
    """A 1-hour-old story with 3 likes beats a 48-hour-old with 20."""
    owner = user_factory("alice")
    now = timezone.now()

    old = story_factory(owner=owner, like_count=20)
    _set_created_at(old, now - timedelta(hours=48))

    new = story_factory(owner=owner, like_count=3)
    _set_created_at(new, now - timedelta(hours=1))

    ids = _feed_ids()
    assert ids.index(new.pk) < ids.index(old.pk)
```

### Score Examples

With this formula (`score = popularity / (age_hours + 2)`):
- 1 hour old, 3 likes: `3 / (1 + 2) = 1.0`
- 48 hours old, 20 likes: `20 / (48 + 2) = 0.4`
- New post wins.

### Why This Works

Time decay without gravity (exponent=1) is simple division. The `+2` denominator offset:
- Prevents near-zero division for posts created just seconds ago
- Keeps brand-new posts from having astronomically high scores
- Creates a "grace period" where scores stabilise before decaying rapidly

---
