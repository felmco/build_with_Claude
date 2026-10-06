# 4.4 Construyendo Servidores MCP

Un Servidor MCP expone "Recursos" (datos de solo lectura), "Prompts" (plantillas) y "Herramientas" (funciones).

## SDK de Python (`mcp`)

```bash
pip install "mcp<2"
```

Los ejemplos de abajo usan la API FastMCP del paquete `mcp` 1.x. En `mcp` 2.x, `FastMCP` pasó a llamarse `MCPServer` (`from mcp.server.mcpserver import MCPServer`); el decorador `@mcp.tool()` y `run()` funcionan igual. Consulta la [documentación del SDK de Python de MCP](https://py.sdk.modelcontextprotocol.io/).

## Ejemplo Mínimo (FastMCP)

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

## Ejecutándolo
Esto se ejecuta sobre Stdio (Entrada/Salida Estándar) por defecto, adecuado para conexiones locales. Nunca uses `print()` hacia stdout en un servidor stdio (corrompe el flujo del protocolo); escribe los logs en stderr. Para servidores remotos usa `mcp.run(transport="streamable-http")`.

## Próximos Pasos
- [Clientes MCP](15_mcp_clientes.md).
