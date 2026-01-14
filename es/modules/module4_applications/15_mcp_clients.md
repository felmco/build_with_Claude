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
Puedes escribir un script de Python para conectarte a un servidor MCP y llamar a sus herramientas programáticamente.

## Próximos Pasos
- [Mejores Prácticas de MCP](./16_mcp_best_practices.md).
