# 4.4 Clientes MCP

Para usar un Servidor MCP, necesitas un cliente.

## 1. Claude Desktop
Configura `claude_desktop_config.json`:

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
¡Claude Desktop ahora verá la herramienta `get_weather`!

## 2. Cliente Python
Puedes escribir un script de Python para conectarte a un servidor MCP y llamar a sus herramientas programáticamente:

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

Para pasar estas herramientas a Claude, convierte cada herramienta MCP en una definición de herramienta de Anthropic (`name`, `description`, `input_schema=tool.inputSchema`) y luego reenvía las llamadas `tool_use` de Claude a `session.call_tool`.

## 3. Conector MCP (servidores remotos)
Para servidores remotos accesibles por HTTP, la API de Mensajes puede conectarse por ti: pasa `mcp_servers=[{"type": "url", "url": "...", "name": "..."}]` y `tools=[{"type": "mcp_toolset", "mcp_server_name": "..."}]` con el beta `mcp-client-2025-11-20` (`client.beta.messages.create(..., betas=["mcp-client-2025-11-20"])`).

## Próximos Pasos
- [Mejores Prácticas de MCP](16_mcp_mejores_practicas.md).
