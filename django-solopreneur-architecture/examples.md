# Examples

## Example: Consolidating FastAPI + MCP Server into Django

### Problem

Architecture had:
- FastAPI backend on port 8000
- MCP server (thin wrapper making HTTP calls to FastAPI)
- LLM orchestrator making HTTP requests to FastAPI
- Separate frontend

This meant 2-3 services to monitor, restart, and debug.

### Solution

Consolidated into single Django application:

```python
# Before: MCP server making HTTP calls
async def get_indicator(symbol: str, interval: str):
    url = f"http://localhost:8000/indicators/rsi"
    params = {"symbol": symbol, "interval": interval}
    response = await httpx.get(url, params=params)
    return response.json()

# After: Django service with in-process calls
class IndicatorService:
    def __init__(self):
        self.api_client = ExternalAPIClient()

    def get_indicator(self, symbol: str, interval: str) -> dict:
        data = self.api_client.get_data(symbol, interval)
        return calculate(data)  # Direct call, no HTTP
```

### Why This Works

- **Single process**: Only Django needs to run (gunicorn/daphne)
- **No HTTP overhead**: Internal calls are Python function calls
- **Easier debugging**: No network layer to troubleshoot
- **Built-in tooling**: Django admin, migrations, ORM
- **Proven deployment**: systemd service is sufficient
