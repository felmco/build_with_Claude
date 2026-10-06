# 2.4 Fundamentos de Streaming

## Introducción
El streaming te permite recibir la respuesta de Claude en tiempo real a medida que se genera, en lugar de esperar a la respuesta completa. Esto crea una mejor experiencia de usuario, especialmente para respuestas largas.

## ¿Por Qué Usar Streaming?

### Beneficios
✅ **Mejor UX**: Los usuarios ven las respuestas inmediatamente
✅ **Velocidad Percibida**: Se siente más rápido aunque el tiempo total sea el mismo
✅ **Retroalimentación en Tiempo Real**: Los usuarios pueden interrumpir si es necesario
✅ **Carga Progresiva**: Muestra el contenido a medida que llega

### Cuándo Usar Streaming
- Chatbots e interfaces conversacionales
- Generación de contenido de formato largo
- Aplicaciones en tiempo real
- Herramientas interactivas
- Cualquier petición con un `max_tokens` grande (aproximadamente por encima de 16K): el SDK rechaza las peticiones largas sin streaming porque corren riesgo de timeouts HTTP, y Opus 5.5 y Fable 5.1 pueden pensar durante minutos en tareas difíciles

### Cuándo NO Usar Streaming
- Procesamiento por lotes
- Pruebas automatizadas
- Cuando necesitas la respuesta completa antes de procesar
- Registro o almacenamiento de respuestas completas

## Ejemplo Básico de Streaming

### Streaming Simple
```python
from anthropic import Anthropic

client = Anthropic()

# client.messages.stream() es un gestor de contexto que maneja la conexión SSE
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Tell me a short story about a robot"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

print()  # Nueva línea al final
```

**Salida** (aparece progresivamente):
```
Once upon a time, there was a small robot named Bolt...
```

### Ejemplo de Streaming Completo con Todos los Eventos
```python
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python in 3 sentences"}
    ]
) as stream:
    # Obtener cada fragmento de texto a medida que llega
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Acceder al mensaje final después de que se complete el streaming
final_message = stream.get_final_message()
print(f"\n\nTokens usados: {final_message.usage.output_tokens}")
```

## Eventos de Stream

### Entendiendo los Eventos de Stream
El streaming proporciona varios tipos de eventos:

```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for event in stream:
        # Tipos de eventos:
        # - message_start: Inicio de respuesta
        # - content_block_start: Inicio de bloque de contenido
        # - content_block_delta: Nuevo fragmento de contenido
        # - content_block_stop: Fin de bloque de contenido
        # - message_delta: Actualización de metadatos del mensaje
        # - message_stop: Fin de respuesta

        print(f"Tipo de evento: {event.type}")
```

### Manejando Diferentes Tipos de Eventos
```python
from anthropic import Anthropic
from anthropic.types import (
    MessageStartEvent,
    ContentBlockStartEvent,
    ContentBlockDeltaEvent,
    ContentBlockStopEvent,
    MessageDeltaEvent,
    MessageStopEvent
)

client = Anthropic()

with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Count to 5"}]
) as stream:
    for event in stream:
        if isinstance(event, MessageStartEvent):
            print("🟢 Mensaje iniciado")
            print(f"   Modelo: {event.message.model}")

        elif isinstance(event, ContentBlockStartEvent):
            print("📝 Bloque de contenido iniciado")

        elif isinstance(event, ContentBlockDeltaEvent):
            # Aquí es donde llega el texto real
            if hasattr(event.delta, 'text'):
                print(event.delta.text, end="", flush=True)

        elif isinstance(event, ContentBlockStopEvent):
            print("\n📝 Bloque de contenido terminado")

        elif isinstance(event, MessageDeltaEvent):
            print(f"🔄 Delta del mensaje: {event.delta.stop_reason}")

        elif isinstance(event, MessageStopEvent):
            print("🔴 Mensaje detenido")
```

## Ayudantes (Helpers) de Stream

### text_stream (Más simple)
Obtener solo el contenido de texto:

```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### get_final_message()
Acceder al mensaje completo después del streaming:

```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Obtener mensaje final con metadatos
message = stream.get_final_message()
print(f"\n\nTokens de entrada: {message.usage.input_tokens}")
print(f"Tokens de salida: {message.usage.output_tokens}")
print(f"Razón de parada: {message.stop_reason}")
```

### get_final_text()
Obtener texto completo después del streaming:

```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Say hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Obtener texto completo
full_text = stream.get_final_text()
print(f"\n\nRespuesta completa: {full_text}")
```

## Patrones Prácticos de Streaming

### Patrón 1: Salida de Consola con Efecto de Escritura
```python
import sys
import time

def stream_with_typing_effect(prompt: str, delay: float = 0.01):
    """Streaming con efecto de escritura"""
    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            sys.stdout.write(text)
            sys.stdout.flush()
            time.sleep(delay)  # Pequeño retraso para efecto de escritura
    print()

# Uso
stream_with_typing_effect("Tell me a joke")
```

### Patrón 2: Streaming con Indicador de Progreso
```python
import sys

def stream_with_progress(prompt: str):
    """Streaming con conteo de caracteres"""
    char_count = 0

    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            char_count += len(text)

    print(f"\n\n📊 Generados {char_count} caracteres")

# Uso
stream_with_progress("Write a paragraph about AI")
```

### Patrón 3: Recolectando Contenido Transmitido
```python
def stream_and_collect(prompt: str) -> tuple[str, dict]:
    """Transmitir texto y recolectar respuesta completa"""
    collected_text = []

    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            collected_text.append(text)

        # Obtener mensaje final
        final_message = stream.get_final_message()

    full_text = "".join(collected_text)
    metadata = {
        "tokens": final_message.usage.output_tokens,
        "stop_reason": final_message.stop_reason
    }

    return full_text, metadata

# Uso
text, meta = stream_and_collect("Explain quantum computing")
print(f"\n\nTokens: {meta['tokens']}")
```

### Patrón 4: Streaming a Archivo
```python
def stream_to_file(prompt: str, filename: str):
    """Transmitir respuesta directamente a archivo"""
    with open(filename, 'w') as f:
        with client.messages.stream(
            model="claude-sonnet-5-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                f.write(text)
                f.flush()  # Asegurar escritura inmediata
                print(text, end="", flush=True)  # También mostrar en pantalla

    print(f"\n\n✅ Guardado en {filename}")

# Uso
stream_to_file("Write a long article about Python", "article.txt")
```

### Patrón 5: Streaming con Manejo de Errores
```python
from anthropic import APIError, APIConnectionError

def safe_stream(prompt: str):
    """Streaming con manejo de errores completo"""
    try:
        with client.messages.stream(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

    except APIConnectionError as e:
        print(f"\n❌ Error de conexión: {e}")
        print("Comprueba tu conexión a internet")

    except APIError as e:
        print(f"\n❌ Error de API: {e}")
        print("Inténtalo de nuevo en un momento")

    except KeyboardInterrupt:
        print("\n\n⚠️  Streaming interrumpido por el usuario")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

# Uso
safe_stream("Tell me about the solar system")
```

## Streaming Asíncrono

### Streaming Asíncrono Básico
```python
import asyncio
from anthropic import AsyncAnthropic

async def async_stream_example():
    """Ejemplo de streaming asíncrono"""
    client = AsyncAnthropic()

    async with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Count to 10"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

    print()

# Ejecutar función asíncrona
asyncio.run(async_stream_example())
```

### Streams Asíncronos Concurrentes
```python
import asyncio
from anthropic import AsyncAnthropic

async def stream_response(client, prompt: str, label: str):
    """Transmitir una única respuesta"""
    print(f"\n{label}:")
    print("-" * 40)

    async with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

    print()

async def concurrent_streams():
    """Ejecutar múltiples streams concurrentemente"""
    client = AsyncAnthropic()

    # Crear múltiples tareas de streaming
    tasks = [
        stream_response(client, "Count to 5", "Stream 1"),
        stream_response(client, "List 3 colors", "Stream 2"),
        stream_response(client, "Name 3 animals", "Stream 3")
    ]

    # Ejecutar todos los streams concurrentemente
    await asyncio.gather(*tasks)

# Ejecutar streams concurrentes
asyncio.run(concurrent_streams())
```

## Construyendo un Chatbot con Streaming

**streaming_chatbot.py**:
```python
#!/usr/bin/env python3
"""Chatbot interactivo con streaming"""

from anthropic import Anthropic
from typing import List, Dict

class StreamingChatbot:
    """Chatbot simple con streaming"""

    def __init__(self):
        self.client = Anthropic()
        self.conversation: List[Dict] = []
        self.model = "claude-sonnet-5-5"

    def chat(self, user_message: str):
        """Enviar mensaje y transmitir respuesta"""
        # Añadir mensaje de usuario a la conversación
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        print("Claude: ", end="", flush=True)

        # Transmitir respuesta
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            messages=self.conversation
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

            # Obtener respuesta completa
            final_message = stream.get_final_message()
            assistant_message = "".join(
                b.text for b in final_message.content if b.type == "text"
            )

        # Añadir respuesta del asistente a la conversación
        self.conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

        print()  # Nueva línea después de la respuesta

def main():
    """Ejecutar chatbot"""
    bot = StreamingChatbot()

    print("Streaming Chatbot (escribe 'quit' para salir)")
    print("=" * 50)

    while True:
        user_input = input("\nTú: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("¡Adiós!")
            break

        if not user_input:
            continue

        try:
            bot.chat(user_input)
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## Consideraciones de Rendimiento

### Tiempo al Primer Token (TTFT)
```python
import time

def measure_streaming_performance(prompt: str):
    """Medir métricas de rendimiento de streaming"""
    start_time = time.time()
    first_token_time = None
    ttft = None
    token_count = 0

    with client.messages.stream(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            if first_token_time is None:
                first_token_time = time.time()
                ttft = first_token_time - start_time
                print(f"⏱️  Tiempo al primer token: {ttft:.2f}s\n")

            print(text, end="", flush=True)
            token_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n\n📊 Rendimiento:")
    print(f"   TTFT: {ttft:.2f}s")
    print(f"   Tiempo total: {total_time:.2f}s")
    print(f"   Fragmentos recibidos: {token_count}")

# Uso
measure_streaming_performance("Explain neural networks")
```

## Problemas Comunes y Soluciones

### Problema 1: Problemas de Búfer
```python
# ❌ Sin flush - puede bufferizar
for text in stream.text_stream:
    print(text)  # Puede no aparecer inmediatamente

# ✅ Con flush - visualización inmediata
for text in stream.text_stream:
    print(text, end="", flush=True)  # Aparece inmediatamente
```

### Problema 2: Problemas con Unicode/Emojis
```python
import sys

# Asegurar codificación adecuada
sys.stdout.reconfigure(encoding='utf-8')

with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Use emojis to describe weather"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Problema 3: Streams Interrumpidos
```python
def handle_interrupted_stream(prompt: str):
    """Manejar interrupción del stream con elegancia"""
    try:
        with client.messages.stream(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

    except KeyboardInterrupt:
        print("\n\n⚠️  Stream interrumpido")
        # Todavía se puede acceder a la respuesta parcial si es necesario
        try:
            partial = stream.get_final_text()
            print(f"Respuesta parcial: {partial}")
        except Exception:
            pass

# Uso
handle_interrupted_stream("Write a long story")
```

## Mejores Prácticas

1. **Usa siempre `flush=True`** para salida inmediata
2. **Maneja interrupciones** con elegancia usando try/except
3. **Usa streaming asíncrono** para peticiones concurrentes
4. **Considera el buffering** para salidas muy rápidas
5. **Monitoriza el rendimiento** (TTFT, throughput)
6. **Prueba con conexiones lentas** para verificar UX
7. **Proporciona retroalimentación** a los usuarios durante el streaming

## Referencia Rápida

```python
# Streaming básico
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Obtener mensaje final
final_message = stream.get_final_message()
print(f"Tokens: {final_message.usage.output_tokens}")
```

## Próximos Pasos
- Aprende [Patrones Avanzados de Streaming](05_streaming_avanzado.md)
- Explora [Visión e Imágenes](06_vision_imagenes.md)
- Construye una [Interfaz Conversacional](03_conversaciones.md)

## Recursos Adicionales
- [Documentación de API de Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Especificación SSE (Server-Sent Events)](https://html.spec.whatwg.org/multipage/server-sent-events.html)
