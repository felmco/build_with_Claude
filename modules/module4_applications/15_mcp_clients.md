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
You can write a Python script to connect to an MCP server and call its tools programmatically.

## Next Steps
- [MCP Best Practices](./16_mcp_best_practices.md).
