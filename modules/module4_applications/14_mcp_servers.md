# 4.4 Building MCP Servers

An MCP Server exposes "Resources" (read-only data), "Prompts" (templates), and "Tools" (functions).

## Python SDK (`mcp`)

```bash
pip install "mcp<2"
```

The examples below use the FastMCP API of the `mcp` 1.x package. In `mcp` 2.x, `FastMCP` was renamed `MCPServer` (`from mcp.server.mcpserver import MCPServer`); the `@mcp.tool()` decorator and `run()` work the same way. See the [MCP Python SDK docs](https://py.sdk.modelcontextprotocol.io/).

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
This runs over Stdio (Standard Input/Output) by default, suitable for local connections. Never `print()` to stdout in a stdio server (it corrupts the protocol stream); log to stderr instead. For remote servers use `mcp.run(transport="streamable-http")`.

## Next Steps
- [MCP Clients](./15_mcp_clients.md).
