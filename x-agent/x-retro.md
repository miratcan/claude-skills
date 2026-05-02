---
name: x-retro
description: >-
  Run a retrospective on recent X posts. Analyzes engagement patterns,
  identifies what works and what doesn't, and updates the posting strategy.
  Use when user says "/x-retro", "X retrospective", "analyze my tweets",
  or "update X strategy". Also triggered automatically by /x-post after
  every 7 posts.
---

# X Agent — Retrospective

Son donem postlarini analiz et, patternleri bul, stratejiyi guncelle.

## Prerequisites

- SQLite DB must have posts and engagement data
- At least 3 posts with engagement data (ideal: 7+)

## Phase 1 — Gather Data

Run Python to get all posts + engagement since last retro:
```
python3 -c "
import sys, json; sys.path.insert(0, 'skills/x-agent')
from db import get_db, init_db, get_posts_since_last_retro, get_latest_engagement, get_active_strategy
init_db()
conn = get_db()
strategy = get_active_strategy(conn)
posts = get_posts_since_last_retro(conn)
data = []
for p in posts:
    eng = get_latest_engagement(conn, p['id'])
    data.append({'post': p, 'engagement': eng})
print('STRATEGY:', json.dumps(strategy['content'], ensure_ascii=False, indent=2))
print('---')
print('POSTS+ENGAGEMENT:', json.dumps(data, ensure_ascii=False, indent=2))
"
```

## Phase 2 — Analyze Patterns

Look at the data and answer these questions:

### Performance by post_type
- Which post_type gets the most replies?
- Which post_type gets the most likes?
- Which post_type triggers the most photo replies?
- Are the strategy weights still correct?

### Content patterns
- What topics/themes got the best engagement?
- What topics/themes underperformed?
- Are there reply patterns (people asking questions back, sharing stories, etc.)?

### Timing
- What time were the best posts posted?
- Does time seem to matter?

### Photo reply analysis
- How many photo replies total?
- Which posts triggered photos and why?
- What made people want to share a photo?

### Audience signals
- Who is replying? (pseudonymous names, profile types)
- Are we reaching our target audience or unrelated demographics?
- Any recurring repliers?

## Phase 3 — Generate Findings

Structure findings as:
```json
{
    "top_performer": {"post_id": N, "content": "...", "why": "..."},
    "worst_performer": {"post_id": N, "content": "...", "why": "..."},
    "patterns": ["pattern 1", "pattern 2"],
    "surprises": ["unexpected finding"],
    "photo_reply_triggers": ["what makes people share photos"],
    "audience_profile": "who is responding"
}
```

## Phase 4 — Update Strategy

Based on findings, create an updated strategy:
1. Adjust post_type weights based on performance
2. Add new examples from successful posts
3. Update "avoid" list with what didn't work
4. Add new learnings
5. Update best_time if data suggests different timing
6. Keep the voice unless there's strong evidence to change it

IMPORTANT: Changes should be incremental. Don't overhaul the entire strategy — adjust 1-2 things per retrospective.

## Phase 5 — Save to DB

```
python3 -c "
import sys, json; sys.path.insert(0, 'skills/x-agent')
from db import get_db, init_db, save_retrospective, create_new_strategy, get_active_strategy, get_posts_since_last_retro
init_db()
conn = get_db()
old_strategy = get_active_strategy(conn)
posts = get_posts_since_last_retro(conn)

new_content = OLD_STRATEGY_CONTENT_WITH_UPDATES
new_strategy_id = create_new_strategy(conn, new_content, parent_id=old_strategy['id'])

findings = FINDINGS_JSON
strategy_changes = CHANGES_JSON

save_retrospective(
    conn,
    period_start=posts[0]['created_at'],
    period_end=posts[-1]['created_at'],
    posts_analyzed=len(posts),
    findings=findings,
    strategy_changes=strategy_changes,
    new_strategy_id=new_strategy_id,
)
print(f'Retrospective saved. New strategy #{new_strategy_id} is now active.')
"
```

## Phase 6 — Report

Present to user:
1. **Period:** date range, N posts analyzed
2. **Top performer:** post content + metrics + why
3. **Key findings:** bullet list
4. **Strategy changes:** what changed and why
5. **Next experiment:** one specific thing to try in the next cycle
