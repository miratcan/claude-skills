---
name: x-check
description: >-
  Check engagement metrics for recent X posts. Reads metrics via Playwright
  browser automation and saves snapshots to SQLite. Use when user says
  "/x-check", "check X engagement", "how are my tweets doing", or
  "engagement report".
---

# X Agent — Engagement Check

Son postlarin engagement metriklerini oku ve kaydet.

## Prerequisites

- Playwright MCP must be available
- User must be logged into X in the browser
- SQLite DB must be initialized

## Phase 1 — Get Posts to Check

Run Python to get recent posts:
```
python3 -c "
import sys, json; sys.path.insert(0, 'skills/x-agent')
from db import get_db, init_db
init_db()
conn = get_db()
rows = conn.execute('SELECT id, content, post_type, x_post_url, posted_at FROM posts ORDER BY posted_at DESC LIMIT 10').fetchall()
for r in rows:
    print(json.dumps(dict(r), ensure_ascii=False))
"
```

## Phase 2 — Read Engagement via Playwright

For each post that has an x_post_url:
1. Navigate to the post URL
2. Take a browser_snapshot
3. Extract from the accessibility tree:
   - Likes count
   - Retweets count
   - Replies count
   - Quote tweets count
   - Impressions (if visible)
4. Scroll through replies:
   - Count total replies visible
   - Count replies that contain photos
   - Save 3-5 interesting reply texts as samples
5. Go back

For posts without x_post_url:
1. Navigate to profile page
2. Find the post by matching content text
3. Click through and read metrics as above

## Phase 3 — Save Engagement Snapshots

For each post checked, run Python to save:
```
python3 -c "
import sys; sys.path.insert(0, 'skills/x-agent')
from db import get_db, init_db, save_engagement
init_db()
conn = get_db()
save_engagement(conn, post_id=POST_ID, likes=N, retweets=N, replies=N, quote_tweets=N, impressions=N, photo_replies_count=N, reply_samples=['sample1', 'sample2'])
print('Saved engagement for post #POST_ID')
"
```

## Phase 4 — Report

Present a summary table:

| Post | Type | Age | Likes | RT | Replies | Photo Replies |
|------|------|-----|-------|----|---------|---------------|
| "..." | daily_question | 3d | 12 | 2 | 8 | 3 |

Highlight:
- Best performing post
- Worst performing post
- Total photo replies (our core metric)
- Any notable replies worth reading
