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
        model="claude-sonnet-4-5-20250929",
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
# (Concepto simplificado)
async with client.messages.stream(..., tools=[...]) as stream:
    for event in stream:
        if event.type == "tool_use":
            # Manejar llamada a herramienta
            pass
        elif event.type == "text_delta":
            # Manejar texto
            pass
```

*Nota: El objeto ayudante `stream` simplifica esto. Acumula las entradas de herramientas automáticamente.*

## Manejo de Errores en Streams

Los errores pueden ocurrir a mitad del stream (ej. desconexión de red).

```python
try:
    with client.messages.stream(...) as stream:
        for text in stream.text_stream:
            print(text)
except anthropic.APIConnectionError:
    print("Stream desconectado. Implementa lógica de reintento aquí.")
```

## Optimizando la Latencia Percibida

1. **Flush (vaciar) la salida inmediatamente:** No almacenes en búfer el texto en tu servidor; envíalo al cliente frontend vía WebSockets o SSE (Eventos Enviados por el Servidor) inmediatamente.
2. **Fragmentos pequeños:** Procesar fragmentos más pequeños actualiza la UI más rápido.

## Ejemplo: Adaptador SSE (Server-Sent Events)

Si estás construyendo un servidor web, a menudo convertirás el stream de Anthropic en un stream SSE para el navegador.

```python
# Pseudo-código para un endpoint Flask/FastAPI
def generate_sse():
    with client.messages.stream(...) as stream:
        for text in stream.text_stream:
            # Formato SSE: "data: <contenido>\n\n"
            yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"
```

## Próximos Pasos
- Explora capacidades multimodales en [Visión e Imágenes](./06_vision_images.md).
