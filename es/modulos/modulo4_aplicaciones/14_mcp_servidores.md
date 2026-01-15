# 4.4 Construyendo Servidores MCP

Un Servidor MCP expone "Recursos" (datos de solo lectura), "Prompts" (plantillas) y "Herramientas" (funciones).

## SDK de Python (`mcp`)

```bash
pip install mcp
```

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
Esto se ejecuta sobre Stdio (Entrada/Salida Estándar) por defecto, adecuado para conexiones locales.

## Próximos Pasos
- [Clientes MCP](15_mcp_clientes.md).
