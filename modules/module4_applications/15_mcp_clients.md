# 4.4 MCP Clients

To use an MCP Server, you need a client.

## 1. Claude Desktop
Configure `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather_server.py"]
    }
  }
}
```
Claude Desktop will now see the `get_weather` tool!

## 2. Python Client
You can write a Python script to connect to an MCP server and call its tools programmatically:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["/path/to/weather_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print([t.name for t in tools.tools])
            result = await session.call_tool("get_weather", {"location": "Paris"})
            print(result.content[0].text)

asyncio.run(main())
```

To pass these tools to Claude, convert each MCP tool to an Anthropic tool definition (`name`, `description`, `input_schema=tool.inputSchema`), then forward Claude's `tool_use` calls to `session.call_tool`.

## 3. MCP Connector (remote servers)
For remote servers reachable over HTTP, the Messages API can connect for you: pass `mcp_servers=[{"type": "url", "url": "...", "name": "..."}]` and `tools=[{"type": "mcp_toolset", "mcp_server_name": "..."}]` with the `mcp-client-2025-11-20` beta (`client.beta.messages.create(..., betas=["mcp-client-2025-11-20"])`).

## Next Steps
- [MCP Best Practices](./16_mcp_best_practices.md).
