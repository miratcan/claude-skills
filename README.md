# Claude Code Skills

A curated collection of [Claude Code](https://claude.ai/code) skills extracted from real development sessions.

Skills are reusable instruction sets that teach Claude Code how to handle specific patterns, avoid known pitfalls, and follow proven approaches. They activate on demand — not loaded into context until triggered.

## Skills

### Django

| Skill | Description |
|-------|-------------|
| [django-solopreneur-architecture](django-solopreneur-architecture/) | Consolidate microservices into a single Django monolith for solo developers |
| [django-god-app-diagnosis](django-god-app-diagnosis/) | Diagnose overgrown Django apps and recommend splitting strategies |
| [django-code-quality-rules](django-code-quality-rules/) | Ruff, pre-commit, vulture, justfile, raw_id_fields — full quality toolchain |
| [django-db-time-decay-scoring](django-db-time-decay-scoring/) | Hacker News-style time decay ranking in Django ORM (SQLite + PostgreSQL) |
| [mypy-strict-django](mypy-strict-django/) | Fix mypy --strict errors in Django projects |
| [code-like-djangonaut](code-like-djangonaut/) | Django conventions: project structure, models, views, admin, Celery, testing |

### UX & Design

| Skill | Description |
|-------|-------------|
| [ux-audit-multidisciplinary](ux-audit-multidisciplinary/) | Multi-expert UX/UI audit framework with 9-section output |
| [ux-walkthrough-report](ux-walkthrough-report/) | Persona-based UX walkthrough with dopamine journey tracking |
| [persona-driven-ux-walkthrough](persona-driven-ux-walkthrough/) | Simulate a user persona browsing a live site via Playwright |
| [ui-mockup-in-html](ui-mockup-in-html/) | Disposable HTML mockups for design exploration before touching real code |

### CSS & Frontend

| Skill | Description |
|-------|-------------|
| [design-tokens](design-tokens/) | Platform-agnostic design token rules: color pairs, opacity ban, minimal scale |
| [semantic-html-css](semantic-html-css/) | Semantic HTML, CSS custom properties, wrapper patterns, scoped selectors |
| [orphan-ui-component-detection](orphan-ui-component-detection/) | Detect React/JS components that are built but never rendered |

### Automation & Tools

| Skill | Description |
|-------|-------------|
| [x-agent](x-agent/) | Autonomous X/Twitter account management with strategy, posting, and engagement tracking |
| [wayback-machine-cdx-crawling](wayback-machine-cdx-crawling/) | Crawl Wayback Machine archives with CDX API and resumable Python crawler |
| [graphify](graphify/) | Transform any input into a knowledge graph with clustered communities |
| [draw-house-svg](draw-house-svg/) | Generate architectural elevation SVG drawings with CAD-level precision |

### Meta

| Skill | Description |
|-------|-------------|
| [skill-structure-creation](skill-structure-creation/) | How to create new Claude Code skills with proper structure |
| [tic80-py2tic](tic80-py2tic/) | TIC-80 fantasy console cartridge editor and Python-to-TIC converter |

## How to Use

Copy a skill directory into your Claude Code skills folder:

```bash
# Find your skills directory
ls ~/.claude/skills/ 2>/dev/null || ls ~/.ccs/instances/*/skills/ 2>/dev/null

# Copy a skill
cp -r django-solopreneur-architecture/ ~/.claude/skills/
```

Or clone the whole repo and symlink what you need.

## Credits

- Most skills by [@miratcan](https://github.com/miratcan)
- [code-like-djangonaut](code-like-djangonaut/) by [@vigo](https://github.com/vigo/claude-skills)
