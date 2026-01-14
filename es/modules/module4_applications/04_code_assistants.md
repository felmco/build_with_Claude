# 4.1 Asistentes de Código

Construir un asistente de codificación requiere estrategias específicas para la generación y comprensión de código.

## Prompt del Sistema para Codificación

```text
You are an expert software engineer.
- Write clean, efficient, documented code.
- Follow PEP 8 for Python.
- Include error handling.
- Explain your logic briefly before writing code.
```

## Conciencia del Contexto
Para editar código existente, debes proporcionar el contenido del archivo.

**Entrada:**
```xml
<file name="main.py">
def hello():
    print("hi")
</file>

Refactor this function to take a name argument.
```

## Técnicas
1. **Relleno en el medio (FIM - Fill-in-the-middle):** No soportado nativamente por la API de Mensajes de Claude, pero puedes simularlo proporcionando "Context Before" y "Context After".
2. **Generación de Pruebas:** Pide a Claude que escriba pruebas *antes* del código (TDD).
3. **Generación de Docstrings:** Envía código, pide documentación.

## Herramientas
- Proporciona una herramienta `read_file` y `write_file` para dejar que Claude edite realmente tu proyecto.

## Próximos Pasos
- Aprende sobre [Arquitectura de Agentes](./05_agent_architecture.md).
