# 2.2 Patrones Avanzados de Streaming

Construyendo sobre los fundamentos, exploremos técnicas avanzadas de streaming para aplicaciones de producción.

## Manejando Eventos de Stream

El gestor de contexto `client.messages.stream()` maneja mucha complejidad por ti. A veces necesitas acceso directo (raw) a los eventos.

### Streaming Asíncrono

Para aplicaciones web de alto rendimiento (FastAPI, Django, etc.), usa el cliente `AsyncAnthropic`.

```python
import asyncio
from anthropic import AsyncAnthropic

async def stream_chat():
    client = AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Tell me a joke"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(stream_chat())
```

## Streaming con Uso de Herramientas

Cuando usas herramientas (function calling) con streaming, necesitas manejar eventos de herramienta.

```python
import anthropic

client = anthropic.Anthropic()

# Define `tools` como en la lección de uso de herramientas
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
) as stream:
    for event in stream:
        if event.type == "content_block_start" and event.content_block.type == "tool_use":
            print(f"Tool call started: {event.content_block.name}")
        elif event.type == "text":
            print(event.text, end="", flush=True)  # evento auxiliar con el fragmento de texto

    # El helper acumula por ti las entradas de herramientas transmitidas
    final = stream.get_final_message()

for block in final.content:
    if block.type == "tool_use":
        print(block.name, block.input)  # entrada completa y ya parseada
```

*Nota: Las entradas de herramientas llegan como JSON parcial (eventos `input_json`). Lee la entrada completa con `get_final_message()` en lugar de parsear los fragmentos tú mismo.*

## Manejo de Errores en Streams

Los errores pueden ocurrir a mitad del stream (ej. desconexión de red).

```python
import anthropic

client = anthropic.Anthropic()

try:
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Tell me a story"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
except anthropic.APIConnectionError:
    # El SDK no reanuda un stream que se corta a mitad. Descarta la salida parcial
    # y reintenta la petición completa (ver la lección de reintentos).
    print("Stream desconectado. Implementa lógica de reintento aquí.")
```

## Optimizando la Latencia Percibida

1. **Flush (vaciar) la salida inmediatamente:** No almacenes en búfer el texto en tu servidor; envíalo al cliente frontend vía WebSockets o SSE (Eventos Enviados por el Servidor) inmediatamente.
2. **Fragmentos pequeños:** Procesar fragmentos más pequeños actualiza la UI más rápido.

## Ejemplo: Adaptador SSE (Server-Sent Events)

Si estás construyendo un servidor web, a menudo convertirás el stream de Anthropic en un stream SSE para el navegador.

```python
import json

# Esquema para un endpoint Flask/FastAPI (envuelve el generador en una respuesta de streaming
# con media_type "text/event-stream")
def generate_sse(prompt: str):
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            # Formato SSE: "data: <contenido>\n\n". Codifica el fragmento como JSON para que los saltos
            # de línea del texto no rompan el formato.
            yield f"data: {json.dumps(text)}\n\n"
    yield "data: [DONE]\n\n"
```

## Próximos Pasos
- Explora capacidades multimodales en [Visión e Imágenes](06_vision_imagenes.md).
