# 2.1 Fundamentos de la API de Mensajes

## Introducción
La API de Mensajes es la interfaz principal para interactuar con Claude. Esta lección cubre todas las características esenciales y mejores prácticas para usar la API de Mensajes de manera efectiva.

## Estructura Básica del Mensaje

### Petición Mínima
```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Petición Completa con Todos los Parámetros
```python
message = client.messages.create(
    # Parámetros requeridos
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],

    # Parámetros opcionales
    system="You are a physics professor explaining concepts simply.",
    # temperature / top_p / top_k: solo en Haiku 4.5 y modelos anteriores
    metadata={"user_id": "user_123"},
    stop_sequences=["Human:", "Assistant:"]
)
```

## Entendiendo los Roles de los Mensajes

### Mensajes de Usuario
Mensajes del usuario a Claude:

```python
messages = [
    {
        "role": "user",
        "content": "What's the weather like?"
    }
]
```

### Mensajes del Asistente
Mensajes de Claude (usados para el historial de conversación):

```python
messages = [
    {
        "role": "user",
        "content": "What's the capital of France?"
    },
    {
        "role": "assistant",
        "content": "The capital of France is Paris."
    },
    {
        "role": "user",
        "content": "What's its population?"
    }
]
```

### Reglas para Roles de Mensajes
1. ✅ Debe empezar con un mensaje de usuario
2. ✅ Debe alternar entre usuario y asistente
3. ✅ Debe terminar con un mensaje de usuario
4. ❌ No puede tener dos mensajes de usuario consecutivos
5. ❌ No puede tener dos mensajes de asistente consecutivos

**Válido**:
```python
messages = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "How are you?"}
]  # ✅ Válido: roles alternos, termina con usuario
```

**Inválido**:
```python
messages = [
    {"role": "user", "content": "Hi"},
    {"role": "user", "content": "Hello?"}  # ❌ Dos mensajes de usuario consecutivos
]

messages = [
    {"role": "assistant", "content": "Hello!"}  # ❌ Empieza con asistente
]
```

## Tipos de Contenido

### Contenido de Texto (Simple)
```python
messages = [
    {
        "role": "user",
        "content": "This is simple text content"
    }
]
```

### Contenido de Texto (Estructurado)
```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Analyze this data and provide insights"
            }
        ]
    }
]
```

### Contenido Multimodal (Texto + Imágenes)
```python
import base64

# Leer archivo de imagen
with open("image.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            }
        ]
    }
]
```

## Prompts del Sistema

Los prompts del sistema proporcionan instrucciones y contexto para el comportamiento de Claude:

### Prompt del Sistema Básico
```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[
        {"role": "user", "content": "How do I read a file in Python?"}
    ]
)
```

### Prompt del Sistema Avanzado con Múltiples Secciones
```python
system_prompt = """You are an expert Python tutor with the following characteristics:

ROLE:
- Patient and encouraging teacher
- Focus on best practices and clean code
- Provide working examples

STYLE:
- Use simple, clear language
- Break down complex concepts
- Include code comments
- Suggest next steps for learning

CONSTRAINTS:
- Always provide complete, runnable code
- Include error handling in examples
- Mention Python version compatibility
- Cite official documentation when relevant
"""

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Teach me about decorators"}
    ]
)
```

## Inmersión Profunda en los Parámetros de la Petición

### max_tokens
Número máximo de tokens en la respuesta:

```python
# Respuesta corta (50-100 tokens ≈ 40-75 palabras)
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Summarize Python in one paragraph"}]
)

# Respuesta media (1000-2000 tokens ≈ 750-1500 palabras)
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2000,
    messages=[{"role": "user", "content": "Explain OOP in Python"}]
)

# Respuesta larga (4000+ tokens ≈ 3000+ palabras)
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a detailed tutorial on async Python"}]
)
```

**Directrices de Tokens**:
- 1 token ≈ 0.75 palabras en inglés
- Máximo: hasta 128K tokens en los modelos actuales (64K en Haiku 4.5); varía según el modelo
- Establecer basado en la longitud de respuesta esperada
- Considerar el coste (cobrado por token de salida)

> ⚠️ **Parámetros de muestreo en los modelos actuales.** Claude Fable 5.1, Opus 5.5 y Sonnet 5.5 no aceptan valores no predeterminados de `temperature`, `top_p` ni `top_k` (la petición devuelve 400). Guía el comportamiento con el prompt y con `output_config.effort`. Los ejemplos siguientes siguen funcionando en **Claude Haiku 4.5** (`claude-haiku-4-5`) y modelos anteriores, por eso lo usan.

### temperature
Controla la aleatoriedad y creatividad (0.0 - 1.0):

```python
# Respuestas deterministas (facuales, consistentes)
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=0.0,  # Más determinista
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

# Respuestas equilibradas (comportamiento por defecto)
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=0.7,  # Equilibrado
    messages=[{"role": "user", "content": "Explain machine learning"}]
)

# Respuestas creativas (variadas, imaginativas)
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=1.0,  # Más creativo
    messages=[{"role": "user", "content": "Write a creative story"}]
)
```

**Directrices de Temperatura**:
| Temperatura | Mejor Para | Casos de Uso de Ejemplo |
|-------------|------------|-------------------------|
| 0.0 - 0.3 | Factual, determinista | Matemáticas, generación de código, Q&A |
| 0.4 - 0.7 | Equilibrado | Chat general, análisis |
| 0.8 - 1.0 | Creativo | Escritura de historias, lluvia de ideas |

### top_p (Nucleus Sampling)
Alternativa a la temperatura para controlar la aleatoriedad:

```python
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    top_p=0.9,  # Considerar el top 90% de masa de probabilidad
    messages=[{"role": "user", "content": "Generate ideas"}]
)
```

**Directrices**:
- Rango: 0.0 - 1.0
- Valores más bajos = más enfocado
- Valores más altos = más diverso
- Usa `temperature` O `top_p`, no ambos

### top_k
Limita el vocabulario a los top K tokens:

```python
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    top_k=40,  # Considerar solo los top 40 tokens en cada paso
    messages=[{"role": "user", "content": "Tell me about AI"}]
)
```

### stop_sequences
Detener la generación cuando se encuentran ciertas secuencias:

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    stop_sequences=["</end>", "STOP", "\n\n---"],
    messages=[{"role": "user", "content": "List 5 programming languages"}]
)
```

**Casos de Uso**:
- Detener en marcadores específicos
- Limitar longitudes de listas
- Controlar formato de salida
- Implementar protocolos personalizados

### metadata
Adjuntar metadatos personalizados para rastreo:

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    metadata={
        "user_id": "user_12345",
        "session_id": "session_abc",
        "environment": "production"
    },
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Estructura de la Respuesta

### Campos Básicos de la Respuesta
```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Campos de respuesta
print(f"ID: {message.id}")                    # ID único del mensaje
print(f"Type: {message.type}")                # Siempre "message"
print(f"Role: {message.role}")                # Siempre "assistant"
print(f"Model: {message.model}")              # Modelo usado
print(f"Content: {message.content}")          # Lista de bloques de contenido
print(f"Stop Reason: {message.stop_reason}")  # Por qué paró la generación
print(f"Stop Sequence: {message.stop_sequence}")  # Si paró por secuencia
print(f"Usage: {message.usage}")              # Info de uso de tokens
```

### Bloques de Contenido
```python
# Bloque de texto único (más común)
message.content[0].type  # "text"
message.content[0].text  # El texto de respuesta real

# Múltiples bloques de contenido (menos común)
for block in message.content:
    if block.type == "text":
        print(f"Text: {block.text}")
```

### Uso de Tokens
```python
# Información de uso detallada
usage = message.usage

print(f"Tokens de entrada: {usage.input_tokens}")
print(f"Tokens de salida: {usage.output_tokens}")
print(f"Tokens totales: {usage.input_tokens + usage.output_tokens}")

# Calcular coste aproximado (tarifas de ejemplo)
INPUT_COST_PER_MTK = 0.003  # Por millón de tokens
OUTPUT_COST_PER_MTK = 0.015  # Por millón de tokens

input_cost = (usage.input_tokens / 1_000_000) * INPUT_COST_PER_MTK
output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_COST_PER_MTK
total_cost = input_cost + output_cost

print(f"Coste estimado: ${total_cost:.6f}")
```

### Razones de Parada
```python
stop_reason = message.stop_reason

# Valores posibles:
# - "end_turn": Completado natural
# - "max_tokens": Alcanzó límite de max_tokens
# - "stop_sequence": Golpeó una secuencia de parada
# - "tool_use": El modelo quiere usar una herramienta (característica avanzada)

if stop_reason == "max_tokens":
    print("⚠️  Respuesta truncada - aumenta max_tokens")
elif stop_reason == "end_turn":
    print("✅ Respuesta completa")
elif stop_reason == "stop_sequence":
    print(f"🛑 Parado en secuencia: {message.stop_sequence}")
```

## Ejemplo Completo: Llamada a la API Estructurada

**structured_api_call.py**:
```python
#!/usr/bin/env python3
"""Ejemplo completo de uso estructurado de la API de Mensajes"""

from anthropic import Anthropic
from typing import Dict, List, Optional
import os

class ClaudeClient:
    """Envoltorio para la API de Mensajes de Claude"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-5-5"

    def send_message(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Enviar un mensaje a Claude y devolver respuesta estructurada

        Args:
            prompt: Mensaje del usuario
            system: Prompt del sistema (opcional)
            max_tokens: Tokens máximos de respuesta
            temperature: Aleatoriedad de respuesta (0.0-1.0)
            conversation_history: Mensajes previos (opcional)

        Returns:
            Dict con texto de respuesta, uso y metadatos
        """
        # Construir lista de mensajes
        messages = conversation_history or []
        messages.append({"role": "user", "content": prompt})

        # Crear petición a la API
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system:
            params["system"] = system

        # Hacer llamada a la API
        message = self.client.messages.create(**params)

        # Devolver respuesta estructurada
        return {
            "text": message.content[0].text,
            "id": message.id,
            "model": message.model,
            "stop_reason": message.stop_reason,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "total_tokens": message.usage.input_tokens + message.usage.output_tokens
            }
        }

def main():
    """Uso de ejemplo"""
    client = ClaudeClient()

    # Petición simple
    response = client.send_message(
        prompt="Explain Python decorators in 2 sentences",
        system="You are a Python expert. Be concise."
    )

    print("Respuesta:")
    print(response["text"])
    print(f"\nTokens usados: {response['usage']['total_tokens']}")

if __name__ == "__main__":
    main()
```

## Mejores Prácticas

### 1. Empieza Simple, Luego Optimiza
```python
# Empieza con valores por defecto
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

# Optimiza basado en necesidades
# - Ajusta max_tokens para longitud de respuesta
# - Establece temperature para creatividad deseada
# - Añade prompts del sistema para controlar el comportamiento
```

### 2. Maneja Siempre los Límites de Tokens
```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

if response.stop_reason == "max_tokens":
    print("Advertencia: La respuesta puede estar incompleta")
    # Considera aumentar max_tokens o dividir la petición
```

### 3. Usa Prompts del Sistema Eficazmente
```python
# ❌ No pongas instrucciones en el mensaje del usuario
messages = [
    {"role": "user", "content": "You are a teacher. Explain photosynthesis."}
]

# ✅ Usa prompt del sistema para instrucciones
system = "You are an experienced biology teacher."
messages = [
    {"role": "user", "content": "Explain photosynthesis."}
]
```

### 4. Estructura Conversaciones de Múltiples Turnos Adecuadamente
```python
# Mantener historial de conversación
conversation = []

# Turno 1
conversation.append({"role": "user", "content": "What's Python?"})
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=conversation
)
conversation.append({"role": "assistant", "content": response.content[0].text})

# Turno 2 (con contexto)
conversation.append({"role": "user", "content": "What are its main uses?"})
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=conversation
)
```

## Próximos Pasos
- Aprende sobre [Prompts del Sistema](02_prompts_sistema.md)
- Explora [Gestionando Conversaciones](03_conversaciones.md)
- Prueba [Respuestas en Streaming](04_conceptos_basicos_streaming.md)

## Recursos Adicionales
- [Documentación Oficial de API de Mensajes](https://platform.claude.com/docs/en/api/messages)
- [Referencia de la API](https://platform.claude.com/docs/en/api/overview)
- [Guía de Mejores Prácticas](https://platform.claude.com/docs/en/build-with-claude/best-practices)
