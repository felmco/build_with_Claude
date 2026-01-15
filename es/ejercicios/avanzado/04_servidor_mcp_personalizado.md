# Ejercicio 4: Servidor MCP Personalizado

## 🎯 Objetivo
Entender el Model Context Protocol (MCP) implementando un servidor básico que exponga recursos locales a Claude.

## ⏱️ Tiempo
60 minutos

## 📚 Requisitos Previos
- Familiaridad con servidores web (conceptos básicos)
- Biblioteca `mcp` (instalar con pip)

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Configurar Servidor
Usa el SDK de MCP para iniciar un servidor.

### Parte 2: Exponer un Recurso
Expone un archivo local (ej., logs del sistema) como un recurso legible por Claude.

### Parte 3: Exponer una Herramienta
Expone una función Python (ej., consultar base de datos SQL) como una herramienta.

### Parte 4: Conectar Cliente
(Opcional) Usa Claude Desktop o un script cliente para conectar a tu servidor.

## 💻 Código de Inicio

```python
from mcp.server import Server

app = Server("mi-demo-mcp")

@app.tool()
def consultar_db(query: str) -> str:
    return "Resultados simulados para " + query

# TODO: Ejecutar servidor
```

## 📖 Resultados de Aprendizaje

- ✅ Estandarización de contexto
- ✅ Arquitectura Cliente-Servidor para IA
