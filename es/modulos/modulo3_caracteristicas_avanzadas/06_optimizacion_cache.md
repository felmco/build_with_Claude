# 3.2 Estrategias de Optimización de Caché

El almacenamiento en caché de prompts reduce costes y latencia, pero solo si se usa correctamente.

## Cómo Funciona el Caché (Repaso)
- **Estructura:** `[Herramientas] -> [Sistema] -> [Mensajes]`
- **Punto de ruptura:** Marcas el *último* bloque que quieres cachear.
- **Vida:** 5 minutos (por defecto), refrescada en cada acierto (hit). Añade `"ttl": "1h"` a `cache_control` para una entrada de 1 hora (el doble de coste de escritura).
- **Límites:** como máximo 4 puntos de ruptura por petición; el prefijo debe alcanzar un mínimo que depende del modelo (de 512 a 4096 tokens) o no se cacheará nada.
- **Coincidencia de prefijo:** cualquier cambio antes de un punto de ruptura (una marca de tiempo, una lista de herramientas distinta, claves JSON reordenadas) invalida ese punto de ruptura y todo lo que va después.

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
Las herramientas se renderizan primero, antes del prompt de sistema. Por tanto, un marcador `cache_control` en el último bloque de sistema cachea juntos las herramientas y el prompt de sistema. También puedes poner el marcador en la última definición de herramienta. Mantén la lista de herramientas idéntica (mismas herramientas, mismo orden) entre peticiones, porque cambiarla invalida todo el caché.

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=TOOLS,  # se renderiza primero
    system=[{"type": "text", "text": LONG_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}}],
    messages=messages,
)
```

## Estrategia 3: Caché Multi-Turno
En una conversación larga, pon un punto de ruptura en el último bloque del turno más reciente para que cada petición lea el historial anterior desde el caché. La forma más sencilla es un `cache_control` de nivel superior, que la API coloca por ti en el último bloque cacheable:

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # punto de ruptura automático en el último bloque cacheable
    messages=messages,
)
```

Para colocarlo tú mismo, convierte primero el contenido del último mensaje en una lista de bloques (el contenido de tipo cadena no tiene lugar para `cache_control`):

```python
last = messages[-1]
if isinstance(last["content"], str):
    last["content"] = [{"type": "text", "text": last["content"]}]
last["content"][-1]["cache_control"] = {"type": "ephemeral"}
```

Los puntos de ruptura anteriores siguen siendo puntos de lectura válidos, pero recuerda el límite de 4 por petición; elimina los marcadores antiguos a medida que añades nuevos.

## Monitorizando Tasa de Aciertos (Hit Rate)
Comprueba las estadísticas de `usage` en la respuesta.
- `cache_creation_input_tokens`: Escritos en caché (se facturan a la tarifa de escritura).
- `cache_read_input_tokens`: Leídos de caché (un acierto).
- `input_tokens`: solo los tokens posteriores al último punto de ruptura, no el total.

**Objetivo:** Maximizar Lectura, Minimizar Creación.

## Próximos Pasos
- Aprende más sobre [Reducción de Costes](07_reduccion_costos.md).
