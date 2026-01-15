# 3.2 Estrategias de Optimización de Caché

El almacenamiento en caché de prompts reduce costes y latencia, pero solo si se usa correctamente.

## Cómo Funciona el Caché (Repaso)
- **Estructura:** `[Herramientas] -> [Sistema] -> [Mensajes]`
- **Punto de ruptura:** Marcas el *último* bloque que quieres cachear.
- **Vida:** 5 minutos (por defecto). Refrescado en cada acierto (hit).

## Estrategia 1: Prefijado Estático
Pon todo el contenido estático en la *parte superior* de tu prompt de sistema o lista de mensajes.

```python
system_content = [
    {
        "type": "text",
        "text": "You are a helpful assistant..."
    },
    {
        "type": "text",
        "text": "<huge_document>...</huge_document>",
        "cache_control": {"type": "ephemeral"} # CACHEAR AQUÍ
    }
]
```

## Estrategia 2: Definiciones de Herramientas
Las herramientas son a menudo estáticas. ¡Cachealas!
*Nota: El cacheo de herramientas usualmente ocurre automáticamente o vía colocación específica dependiendo de actualizaciones de la API. Comprueba la documentación actual.*

## Estrategia 3: Caché Multi-Turno
En una conversación larga, cachea el *último* mensaje periódicamente (ej. cada 5 turnos) para crear puntos de control.

```python
# Pseudo-código
messages = [...]
if len(messages) % 5 == 0:
    messages[-1]["content"][0]["cache_control"] = {"type": "ephemeral"}
```

## Monitorizando Tasa de Aciertos (Hit Rate)
Comprueba las estadísticas de `usage` en la respuesta.
- `cache_creation_input_tokens`: Fallo (Escrito en caché).
- `cache_read_input_tokens`: Acierto (Leído de caché).

**Objetivo:** Maximizar Lectura, Minimizar Creación.

## Próximos Pasos
- Aprende más sobre [Reducción de Costes](07_reduccion_costos.md).
