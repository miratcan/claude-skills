---
name: django-solopreneur-architecture
description: |
  Avoid multi-service architecture complexity for solo developers. Consolidate FastAPI,
  separate MCP servers, and microservices into a single Django monolith with repository pattern.
  Use when: designing architecture for solo-built web apps, considering FastAPI + separate services,
  or user says "I don't want to monitor multiple services" or "always bet on Django".
---

# Django Solopreneur Architecture

## When to Use

Use this pattern when:
- Solo developer or small team (1-3 people)
- Don't want to monitor multiple services
- Architecture involves FastAPI + separate MCP server + separate workers
- Want "old school deployment" without Docker/Kubernetes orchestration
- VPS with Redis, PostgreSQL, and minimal overhead

## Instructions

### 1. Consolidate into Single Django Application

Instead of:
```
project/
├── api/           # FastAPI backend
├── mcp/           # Separate MCP server
├── workers/       # Celery or similar
└── frontend/      # Separate Next.js deployment
```

Do this:
```
project/
├── backend/       # Single Django app
│   ├── api/       # Django REST endpoints
│   ├── services/  # Business logic (repository pattern)
│   ├── chat/      # Django Channels for WebSocket
│   └── tasks/     # Celery tasks (if needed)
└── frontend/      # Can stay separate (Vercel/CDN)
```

### 2. Use Service/Repository Pattern

Move external API logic into Django services:

```python
# backend/services/data_provider.py
class DataProviderService:
    def __init__(self):
        self.api_client = ExternalAPIClient()

    def get_data(self, key: str) -> dict:
        return self.api_client.fetch(key)

    def get_computed(self, key: str, method: str) -> dict:
        # Direct in-process call, no HTTP
        return self.compute_service.calculate(key, method)
```

### 3. Replace HTTP Internal Calls with In-Process

```python
# WRONG: internal HTTP calls between components
async def get_data():
    response = await httpx.get("http://localhost:8000/data/key")
    return response.json()

# CORRECT: direct in-process service call
def get_data():
    service = DataProviderService()
    return service.get_data("key")
```

### 4. Deployment Philosophy

For solopreneurs on VPS with existing PostgreSQL, Redis, Caddy:
- **No Docker** unless specifically needed (lower overhead)
- **systemd** for process management
- **Gunicorn/uWSGI** for Django
- **Daphne** for Django Channels (WebSocket)
- **Caddy** for reverse proxy

Example systemd service:
```ini
[Unit]
Description=Django Backend
After=network.target postgresql.service redis.service

[Service]
User=www-data
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/gunicorn project.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Failed Attempts

| What Was Tried | Why It Failed |
|----------------|---------------|
| FastAPI + separate MCP server | Two processes to monitor/restart. If one fails, system breaks silently. Solo devs can't afford multi-service babysitting. |
| Microservices "for scalability" with <100 users | Premature optimization. Added complexity for zero benefit. Monolith until actual scale problems. |
| Docker Compose on small VPS | Extra memory overhead, debugging complexity, slower deploys. systemd was already working fine. |

## Common Mistakes

- **Don't** split services "because it's more professional" — start with monolith, extract only when pain is real
- **Don't** make internal HTTP calls between components — use direct Python imports
- **Don't** default to Docker — ask about existing infrastructure first
- **Don't** assume "modern" architecture is wanted — experienced devs often prefer boring, proven solutions
