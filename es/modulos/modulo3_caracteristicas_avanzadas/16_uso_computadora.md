# 3.6 Uso de Computadora (Beta)

Claude puede controlar el escritorio de una computadora (ratón, teclado, capturas de pantalla).

## Requisitos Previos
- **Docker:** Ejecuta el contenedor de referencia de Anthropic.
- **Encabezado Beta:** `computer-use-2025-01-24` (o el más reciente).

## La Definición de la Herramienta

A diferencia de las herramientas estándar, "computer" es un tipo de herramienta incorporada.

```python
tools = [
    {
        "type": "computer_20250124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1
    }
]
```

## Cómo Funciona
1. Claude envía una petición de uso de herramienta (ej. `screenshot`, `mouse_move`, `type`).
2. Tu "Bucle de Agente" ejecuta esto en la VM/Contenedor.
3. Envías el resultado (imagen o estado) de vuelta a Claude.

*Nota: Esto requiere un entorno especializado. Ver la Implementación de Referencia.*

## Próximos Pasos
- [Automatización de Computadora](17_automatizacion_computadora.md).
