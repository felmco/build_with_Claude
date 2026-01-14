# 4.4 Protocolo de Contexto de Modelo (MCP)

**MCP** es un estándar abierto que permite a los asistentes de IA interactuar con tus datos y herramientas de una manera estandarizada.

## ¿Por qué MCP?
- **Interfaz Unificada:** Conecta Claude Desktop, IDEs y Chatbots a las mismas fuentes de datos (Google Drive, Slack, Postgres).
- **Sin Fragmentación:** Construye una herramienta una vez, úsala en todas partes.

## Arquitectura
- **Servidor MCP:** Expone datos/herramientas (ej. un envoltorio de base de datos SQLite).
- **Cliente MCP:** La aplicación de IA (ej. Claude Desktop, o tu aplicación Python).
- **Host:** El entorno de ejecución.

## Recursos
- [Documentación Oficial](https://modelcontextprotocol.io/docs/getting-started/intro).

## Próximos Pasos
- [Construyendo Servidores MCP](./14_mcp_servers.md).
