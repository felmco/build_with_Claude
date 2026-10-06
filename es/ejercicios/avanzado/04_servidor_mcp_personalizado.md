# Ejercicio 4: Servidor MCP Personalizado

## 🎯 Objetivo
Entender el Model Context Protocol (MCP) implementando un servidor básico que exponga recursos locales a Claude.

## ⏱️ Tiempo
60+ minutos

## 📚 Requisitos Previos
- Familiaridad con servidores web (conceptos básicos)
- Paquete oficial `mcp` de Python (instalar con pip)

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Configurar Servidor
Usa el SDK de MCP (`FastMCP`) para iniciar un servidor.

### Parte 2: Exponer un Recurso
Expone un archivo local (ej., logs del sistema) como un recurso legible por Claude.

### Parte 3: Exponer una Herramienta
Expone una función Python (ej., consultar base de datos SQL) como una herramienta.

### Parte 4: Conectar Cliente
(Opcional) Usa Claude Desktop o un script cliente para conectar a tu servidor.

## 💻 Código de Inicio

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b

# TODO: añade tus propias herramientas (por ejemplo consultar_db)

if __name__ == "__main__":
    mcp.run()
```

## 🎁 Pistas

Usa el paquete oficial `mcp` de Python: `from mcp.server.fastmcp import FastMCP`, crea `mcp = FastMCP("nombre")`, decora las funciones con `@mcp.tool()` y ejecuta con `mcp.run()`. Pruébalo con el MCP Inspector o con Claude Desktop. Consulta modelcontextprotocol.io para ver la documentación actual.

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
# Esquema de referencia: amplía el servidor FastMCP anterior con herramientas que envuelvan una API real
# (por ejemplo consultas meteorológicas), valida las entradas y devuelve mensajes de error claros.
```
</details>

## 📖 Resultados de Aprendizaje

- ✅ Estandarización de contexto
- ✅ Arquitectura Cliente-Servidor para IA
