---
name: x-post
description: >-
  Autonomous X (Twitter) account management agent. Reads current strategy
  from SQLite, generates a post, publishes via Playwright browser automation,
  and tracks engagement of previous posts.
  Use when user says "/x-post", "post to X", "tweet something", or
  "run the daily X post".
---

# X Agent — Daily Post

Otonom X hesap yonetimi. Strateji oku → post uret → Playwright ile at → engagement takip et.

## Prerequisites

- Playwright MCP must be available
- User must be logged into X in the browser Playwright controls
- SQLite DB must be initialized

## Phase 1 — Initialize

1. Run `python3 skills/x-agent/db.py` to ensure DB exists
2. Read active strategy from DB:
   `python3 -c "import sys; sys.path.insert(0, 'skills/x-agent'); from db import get_db, init_db, get_active_strategy; init_db(); conn = get_db(); s = get_active_strategy(conn); print(s['content'])"`

## Phase 2 — Generate Post

Based on the active strategy:
1. Pick a post_type using the weights (e.g. 50% daily_question, 30% observation, 20% nostalgia)
2. Generate a NEW post that:
   - Matches the voice described in strategy
   - Is the chosen post_type
   - Is NOT a copy of the examples (use them as inspiration)
   - Is max 200 characters (Turkish)
   - Aims to trigger photo replies
   - Avoids everything in the "avoid" list
3. Show the generated post to the conversation and note the post_type

## Phase 3 — Publish via Playwright

1. Navigate to https://x.com/compose/post (or https://x.com and click compose)
2. Take a browser_snapshot to verify login state
3. If not logged in: STOP and tell user "X'e giris yapilmamis. Lutfen browser'da X'e login ol."
4. Type the post content into the compose box
5. Click the "Post" / "Gonder" button
6. Wait 3 seconds for post to publish
7. Take a snapshot to verify post was published
8. Try to capture the post URL from the page

## Phase 4 — Save to DB

Run Python to save the post:
```
python3 -c "
import sys; sys.path.insert(0, 'skills/x-agent')
from db import get_db, init_db, save_post, get_active_strategy
init_db()
conn = get_db()
strategy = get_active_strategy(conn)
post_id = save_post(conn, content='POST_CONTENT_HERE', post_type='TYPE_HERE', strategy_id=strategy['id'], x_post_url='URL_OR_NONE')
print(f'Saved post #{post_id}')
"
```

## Phase 5 — Check Previous Posts' Engagement

1. Navigate to the profile page on X
2. For each of the last 5 posts (that have been posted 24h+ ago):
   a. Click on the post to see its detail page
   b. Read engagement metrics from the snapshot (likes, retweets, replies)
   c. Note if any replies contain photos
   d. Go back to profile
3. Save engagement snapshots to DB for each post

## Phase 6 — Retrospective Check

1. Count posts since last retrospective:
   `python3 -c "import sys; sys.path.insert(0, 'skills/x-agent'); from db import get_db, init_db, count_posts_since_last_retro; init_db(); conn = get_db(); print(count_posts_since_last_retro(conn))"`
2. If >= 7: trigger retrospective (follow /x-retro flow)
3. If < 7: report "N/7 posts until next retrospective"

## Output

Summarize:
- What was posted (content + type)
- Engagement update for previous posts (if any checked)
- Retrospective status (N/7)
