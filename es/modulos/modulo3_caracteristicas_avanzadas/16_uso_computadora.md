# 3.6 Uso de Computadora

Claude puede controlar un escritorio (ratón, teclado, capturas de pantalla).

## Requisitos Previos
- **Docker:** Ejecuta el contenedor de referencia de Anthropic (o tu propia VM aislada).
- **Sin cabecera beta:** `computer_toolset_20260801` está disponible de forma general en la Claude API y Google Cloud.

## La Definición de la Herramienta

A diferencia de las herramientas estándar, el toolset de computadora está integrado en el modelo y no requiere esquema. Expone 17 herramientas miembro (`screenshot`, `zoom`, `left_click`, `type`, `key`, `scroll`, `wait`, ...).

```python
tools = [
    {"type": "computer_toolset_20260801"},
    # Ajustes opcionales por miembro:
    # {"type": "computer_toolset_20260801", "configs": {"zoom": {"enabled": False}}},
]
```

> **¿Migrando?** La herramienta anterior `computer_20251124` (con `display_width_px` y cabecera beta) está obsoleta en los modelos Claude 5.5 y devuelve 400 en la Claude API y Google Cloud con Opus 5.5 / Sonnet 5.5. No pueden mezclarse en una misma petición. Consulta la [documentación de uso de computadora](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).

## Cómo Funciona
1. Claude envía una solicitud de uso de herramienta (p. ej. `screenshot`, `left_click`, `type`).
2. Tu "Bucle de Agente" la ejecuta en la VM/contenedor.
3. Devuelves el resultado con `"toolset_name": "computer"` en el `tool_result` (un bloque de imagen para `screenshot` y `zoom`, texto en el resto).

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01...",
  "toolset_name": "computer",
  "content": [{ "type": "text", "text": "OK" }]
}
```

*Nota: Requiere un entorno especializado y aislado. Consulta la Implementación de Referencia y mantén a una persona en el bucle para acciones sensibles.*

## Próximos Pasos
- [Automatización de Computadora](17_automatizacion_computadora.md).
