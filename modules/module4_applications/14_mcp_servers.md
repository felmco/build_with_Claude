# 4.4 Building MCP Servers

An MCP Server exposes "Resources" (read-only data), "Prompts" (templates), and "Tools" (functions).

## Python SDK (`mcp`)

```bash
pip install mcp
```

## Minimal Example (FastMCP)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Weather Server")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get weather for a location"""
    return f"Weather in {location} is sunny."

if __name__ == "__main__":
    mcp.run()
```

## Running it
This runs over Stdio (Standard Input/Output) by default, suitable for local connections.

## Next Steps
- [MCP Clients](./15_mcp_clients.md).
