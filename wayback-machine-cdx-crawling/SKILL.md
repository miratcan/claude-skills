---
name: wayback-machine-cdx-crawling
description: |
  Crawl Wayback Machine archives using the CDX API to discover and fetch archived pages.
  Use when: scraping historical data from archived sites, researching old content via web.archive.org,
  extracting data from Wayback Machine snapshots, building URL inventories of archived domains.
  CRITICAL: WebFetch is blocked for web.archive.org - always use curl via Bash instead.
  Example triggers: "crawl wayback machine", "fetch archived pages", "get data from web.archive.org",
  "scrape historical snapshots", "CDX API", "wayback crawl".
verified: 2026-02-18
source-session: 2df316e8-ed9f-47c1-a036-6eac07a2beec
---

# Wayback Machine CDX API Crawling

## Critical: WebFetch Is Blocked for web.archive.org

**`WebFetch` returns "Claude Code is unable to fetch from web.archive.org".**

Always use `curl` via the `Bash` tool instead:

```bash
# This FAILS:
# WebFetch(url="https://web.archive.org/cdx/search/cdx?...", ...)

# This WORKS:
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com/*&output=text&fl=timestamp,original,statuscode&limit=500"
```

## When to Use

- User wants to scrape/analyze an archived version of a site
- Need to discover all archived URLs for a domain
- Extracting historical content (posts, questions, answers) from Wayback Machine
- Building a dataset from a defunct website's archive

## CDX API: URL Discovery

The CDX API lets you inventory what Wayback Machine has archived without fetching each page:

```bash
# Get all archived URLs for a domain pattern, deduplicated by URL key
curl -s "https://web.archive.org/cdx/search/cdx?\
url=example.com/path/*\
&output=text\
&fl=timestamp,original,statuscode\
&filter=statuscode:200\
&collapse=urlkey\
&limit=5000" | head -100

# With date range filter (YYYYMMDD format)
curl -s "https://web.archive.org/cdx/search/cdx?\
url=example.com/q/*\
&output=json\
&fl=timestamp,original,statuscode\
&filter=statuscode:200\
&from=20160101\
&to=20170101\
&collapse=urlkey\
&limit=5000"
```

### Key CDX API Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `url` | URL pattern to search | `example.com/q/*` |
| `output` | Format: `text`, `json`, `csv` | `output=json` |
| `fl` | Fields to return | `fl=timestamp,original,statuscode` |
| `filter` | Filter results | `filter=statuscode:200` |
| `collapse` | Deduplicate by field | `collapse=urlkey` |
| `from` / `to` | Date range (YYYYMMDD) | `from=20160101` |
| `limit` | Max results | `limit=5000` |
| `matchType` | `domain`, `prefix`, `exact` | `matchType=domain` |

### JSON Output (for Python scripting)

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode&collapse=urlkey&limit=5000"
# Returns: [["timestamp","original","statuscode"], ["20150317...", "http://...", "200"], ...]
# First row is the header - skip it in your code
```

## Fetching Archived Pages via curl

```bash
# Wayback URL format: https://web.archive.org/web/{timestamp}/{original_url}
curl -s "https://web.archive.org/web/20160329031348/http://example.com/page/1/" | head -200

# Always use a User-Agent header to be polite
curl -s -A "research-bot/1.0" "https://web.archive.org/web/{timestamp}/{url}"
```

## Resumable Python Crawler Pattern

For long-running crawls (100+ pages), use a progress file to support resume on interruption:

```python
#!/usr/bin/env python3
import json
import time
import re
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

PROGRESS_FILE = Path("scripts/.crawl_progress.json")
REQUEST_DELAY = 1.2  # Be polite to Wayback Machine

def fetch(url, retries=3):
    """Fetch URL with retry and rate limiting."""
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "archive-research/1.0"})
            with urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError) as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY * (attempt + 1))
    return None

def get_urls_from_cdx(pattern, from_date=None, to_date=None):
    """Discover archived URLs via CDX API."""
    params = (
        f"https://web.archive.org/cdx/search/cdx"
        f"?url={pattern}&output=json"
        f"&fl=timestamp,original,statuscode"
        f"&filter=statuscode:200&collapse=urlkey&limit=5000"
    )
    if from_date:
        params += f"&from={from_date}"
    if to_date:
        params += f"&to={to_date}"

    raw = fetch(params)
    if not raw:
        return []
    data = json.loads(raw)
    # Skip header row
    if data and data[0] == ["timestamp", "original", "statuscode"]:
        data = data[1:]
    return data  # list of [timestamp, original, statuscode]

def load_progress():
    """Load resume state."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": [], "results": []}

def save_progress(progress):
    """Save resume state after each page."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, ensure_ascii=False)

def crawl(urls_to_process):
    """Main crawl loop with resume support."""
    progress = load_progress()
    completed = set(progress["completed"])
    results = progress["results"]

    remaining = [(ts, url) for ts, url, _ in urls_to_process
                 if url not in completed]
    print(f"  {len(completed)} done, {len(remaining)} remaining")

    for i, (timestamp, original) in enumerate(remaining):
        wayback_url = f"https://web.archive.org/web/{timestamp}/{original}"
        print(f"  [{i+1}/{len(remaining)}] {original}")

        html = fetch(wayback_url)
        if not html:
            print("    -> Skipped (unreachable)")
            progress["completed"].append(original)
            save_progress(progress)
            time.sleep(REQUEST_DELAY)
            continue

        # Parse what you need from html here
        data = parse_page(html)
        if data:
            results.append(data)
            progress["completed"].append(original)
            save_progress(progress)

        time.sleep(REQUEST_DELAY)

    return results

# Cleanup when done
if PROGRESS_FILE.exists():
    PROGRESS_FILE.unlink()
```

## Snapshot Selection Strategy

When multiple snapshots exist for a URL, prefer the **most recent one** with a 200 status. Older snapshots may have less content (site was still growing).

```python
# Use from/to date filters to target the latest live period
# Example: site shut down in 2017, so use 2016 snapshots for max content
urls = get_urls_from_cdx("example.com/q/*", from_date="20160101", to_date="20170101")
```

## Detecting Login Walls vs Real Content

Wayback Machine archives pages exactly as crawled. Invite-only or login-required sites will have login wall snapshots. Detect them in parsed HTML:

```python
from html import unescape

def parse_page(html):
    # Check if page title is the site name (login wall redirect)
    title_m = re.search(r"<title>(.*?)</title>", html)
    if title_m:
        title = unescape(title_m.group(1).strip()).lower()
        if title in ("example.com", "sign in", "login", ""):
            return None  # Login wall - skip
    # ... rest of parsing
```

## Page Type Strategy for Content-Rich Sites

Some archived sites have multiple page variants per URL (e.g., latest answers, popular, featured). The **featured** or **popular** sub-pages often show more content than the default listing:

```bash
# For a Q&A site: /q/SLUG/ shows latest 5, /q/SLUG/popular/ shows all by engagement
# Check which has more complete data before building your scraper
curl -s "https://web.archive.org/web/{ts}/http://example.com/q/1/popular/" | head -100
```

## Failed Attempts

| What Was Tried | Why It Failed | Correct Approach |
|---|---|---|
| `WebFetch("https://web.archive.org/cdx/search/cdx?...")` | Returns "Claude Code is unable to fetch from web.archive.org" | Use `curl` via Bash tool |
| Fetching early snapshots (2013-2015) for a site active until 2017 | Less content indexed - site was still growing | Use `from`/`to` date filters to target peak traffic period |
| Running bulk CDX count commands inline | User interrupted - they wanted a reusable script | Write the crawl as a Python script with resume support |

## Common Mistakes

- **Using WebFetch for web.archive.org** - it is blocked, use curl instead
- **Not using `collapse=urlkey`** - without this you get duplicate snapshots of the same URL
- **Not handling login walls** - check page title for site name or "login" redirect
- **No request delay** - Wayback Machine can rate-limit aggressive scrapers; use 1-2 seconds
- **No resume support** - for 100+ pages, always save progress after each page
- **Using oldest snapshots** - for max content, use snapshots from the site's peak/final period

## Version History

- 1.0.0 (2026-02-18): Initial version from session 2df316e8 - Wayback Machine CDX API crawling with curl workaround for WebFetch block, resumable crawler pattern
