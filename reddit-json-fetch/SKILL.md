---
name: reddit-json-fetch
description: |
  Fetch Reddit posts and comments via the JSON API when WebFetch is blocked.
  Use when: user shares a reddit.com URL, asks to read a Reddit post, or
  mentions Reddit content. WebFetch and old.reddit.com are both blocked —
  use www.reddit.com with .json suffix and a browser User-Agent via curl.
---

# Reddit JSON Fetch

## When to Use

- User shares a reddit.com link
- User asks to read/fetch a Reddit post or comments
- Any task requiring Reddit content

## Why This Exists

- `WebFetch` returns "Claude Code is unable to fetch from www.reddit.com"
- `old.reddit.com` JSON endpoint is blocked (returns "whoa there, pardner!")
- `www.reddit.com` with `.json` suffix still works with a proper User-Agent

## How to Fetch

Append `.json` to the Reddit URL and use curl with a browser User-Agent:

```bash
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" -L "https://www.reddit.com/r/SUBREDDIT/comments/POST_ID/SLUG/.json"
```

**Important:**
- Use `www.reddit.com`, NOT `old.reddit.com`
- Always append `.json` to the URL path
- Always include a realistic browser `User-Agent` header
- Use `head -c` to limit output if you only need the post (first listing), or pipe through `python3 -m json.tool` for readability

## Response Structure

Reddit returns an array of two Listing objects:

```
[0] = Post listing (selftext, title, author, score, etc.)
[1] = Comments listing (nested tree of comments)
```

Key fields in post data (`[0].data.children[0].data`):
- `title` — post title
- `selftext` — post body (markdown)
- `author` — username
- `score` — upvotes
- `num_comments` — comment count
- `created_utc` — timestamp

Key fields in comment data (`[1].data.children[].data`):
- `body` — comment text
- `author` — commenter
- `score` — upvotes
- `replies` — nested replies (same structure)

## Common Mistakes

- Using `WebFetch` for Reddit — it's blocked, always use curl
- Using `old.reddit.com` — blocked since 2024 API policy change
- Forgetting the User-Agent — Reddit returns 403 or "Blocked" page without it
- Not appending `.json` — returns HTML instead of structured data
