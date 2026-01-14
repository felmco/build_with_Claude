# 4.4 Model Context Protocol (MCP)

**MCP** is an open standard that enables AI assistants to interact with your data and tools in a standardized way.

## Why MCP?
- **Unified Interface:** Connect Claude Desktop, IDEs, and Chatbots to the same data sources (Google Drive, Slack, Postgres).
- **No Fragmentation:** Build a tool once, use it everywhere.

## Architecture
- **MCP Server:** Exposes data/tools (e.g., a SQLite database wrapper).
- **MCP Client:** The AI application (e.g., Claude Desktop, or your Python app).
- **Host:** The runtime environment.

## Resources
- [Official Docs](https://modelcontextprotocol.io/docs/getting-started/intro).

## Next Steps
- [Building MCP Servers](./14_mcp_servers.md).
