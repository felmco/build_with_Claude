# 3.2 Entendiendo el Almacenamiento en Caché de Prompts

## Introducción
El almacenamiento en caché de prompts permite reutilizar grandes porciones de tu prompt a través de múltiples peticiones, reduciendo drásticamente los costes (hasta un 90%) y la latencia (hasta un 80%) para contenido repetido.

## ¿Por Qué Almacenamiento en Caché de Prompts?

### Sin Caché
Cada llamada a la API procesa el prompt completo desde cero:
```
Petición 1: Procesa 10,000 tokens → Coste total
Petición 2: Procesa 10,000 tokens → Coste total (¡mismo contenido!)
Petición 3: Procesa 10,000 tokens → Coste total (¡mismo contenido!)
```

### Con Caché
Reutiliza porciones cacheadas:
```
Petición 1: Procesa 10,000 tokens → Cachéalos → Coste total
Petición 2: Lee de caché → ¡90% reducción de coste!
Petición 3: Lee de caché → ¡90% reducción de coste!
```

## Comparación de Costes

### Precios (Aproximados)
- **Tokens de entrada regulares**: $3 por millón de tokens
- **Escritura en caché**: $3.75 por millón de tokens (25% más)
- **Lectura de caché**: $0.30 por millón de tokens (¡90% menos!)

### Ejemplo de Cálculo
Prompt de 10,000 tokens, usado 100 veces:

**Sin caché**:
```
100 peticiones × 10,000 tokens × $3/MTok = $3.00
```

**Con caché**:
```
Escritura: 1 × 10,000 × $3.75/MTok = $0.0375
Lecturas: 99 × 10,000 × $0.30/MTok = $0.297
Total: $0.0375 + $0.297 = $0.3345
Ahorro: $3.00 - $0.33 = $2.67 (¡89% reducción!)
```

## Cómo Funciona el Caché de Prompts

### Puntos de Ruptura de Caché (Breakpoints)
Marca el contenido a ser cacheado usando `cache_control`:

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant with access to the following documentation...",
        },
        {
            "type": "text",
            "text": "<long documentation content here>",
            "cache_control": {"type": "ephemeral"}  # ¡Cachea esto!
        }
    ],
    messages=[
        {"role": "user", "content": "Based on the docs, explain feature X"}
    ]
)
```

### Duración del Caché
- **Duración**: 5 minutos
- **Actualización**: Cada acierto de caché (hit) extiende la duración por 5 minutos
- **Máximo**: Los cachés duran tanto como se usen dentro de ventanas de 5 minutos

## Ejemplo Básico de Caché

**simple_caching.py**:
```python
#!/usr/bin/env python3
"""Ejemplo básico de caché de prompts"""

from anthropic import Anthropic
import time

client = Anthropic()

# Base de conocimiento grande para cachear
KNOWLEDGE_BASE = """
Python Programming Guide:
=========================

1. Variables and Data Types:
   - Strings: text data enclosed in quotes
   - Integers: whole numbers
   - Floats: decimal numbers
   - Lists: ordered collections [1, 2, 3]
   - Dictionaries: key-value pairs {"key": "value"}

2. Control Flow:
   - if/elif/else: conditional execution
   - for loops: iterate over sequences
   - while loops: repeat while condition is true

3. Functions:
   - def function_name(parameters):
   - return values
   - *args and **kwargs for flexible parameters

4. Classes:
   - class ClassName:
   - __init__ method for initialization
   - self parameter for instance reference

[... imagina que esto son 10,000+ tokens de documentación ...]
"""

def ask_with_caching(question: str):
    """Preguntar con base de conocimiento cacheada"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a Python programming expert. Use the following documentation to answer questions:"
            },
            {
                "type": "text",
                "text": KNOWLEDGE_BASE,
                "cache_control": {"type": "ephemeral"}  # Cachear este bloque
            }
        ],
        messages=[
            {"role": "user", "content": question}
        ]
    )

    # Comprobar uso de caché
    usage = response.usage
    print(f"""
 📊 Uso de Tokens:
    Tokens entrada: {usage.input_tokens}
    Creación caché: {getattr(usage, 'cache_creation_input_tokens', 0)}
    Lectura caché: {getattr(usage, 'cache_read_input_tokens', 0)}
    Tokens salida: {usage.output_tokens}
    """)

    return response.content[0].text

def main():
    """Probar caché con múltiples peticiones"""

    questions = [
        "What are Python data types?",
        "Explain Python functions",
        "How do classes work in Python?",
        "What are control flow statements?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Petición #{i}: {question}")
        print('='*60)

        answer = ask_with_caching(question)
        print(f"\n💬 Respuesta: {answer}")

        if i < len(questions):
            print("\n⏳ Esperando 1 segundo...")
            time.sleep(1)  # Pequeño retraso entre peticiones

if __name__ == "__main__":
    main()
```

## Cacheando Prompts del Sistema

### Prompt del Sistema Único
```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Very long system instructions...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)
```

### Múltiples Bloques del Sistema
```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "General instructions (not cached)",
        },
        {
            "type": "text",
            "text": "Large knowledge base part 1...",
            "cache_control": {"type": "ephemeral"}  # Punto de caché 1
        },
        {
            "type": "text",
            "text": "Large knowledge base part 2...",
            "cache_control": {"type": "ephemeral"}  # Punto de caché 2
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)
```

## Cacheando Historial de Conversación

### Cacheando Conversaciones Largas
```python
def chat_with_caching(messages: list, new_message: str):
    """Chat con historial de conversación cacheado"""

    # Añadir nuevo mensaje de usuario
    messages.append({
        "role": "user",
        "content": new_message
    })

    # Marcar los últimos turnos para caché (contexto de conversación)
    # Clonar mensajes para evitar modificar original
    cached_messages = messages[:-1]  # Todo menos el último mensaje
    if cached_messages:
        # Añadir control de caché al último mensaje antes del actual
        last_msg = cached_messages[-1].copy()
        if isinstance(last_msg["content"], str):
            last_msg["content"] = [
                {
                    "type": "text",
                    "text": last_msg["content"],
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        cached_messages[-1] = last_msg

    # Añadir mensaje actual sin control de caché
    cached_messages.append(messages[-1])

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=cached_messages
    )

    # Añadir respuesta del asistente al historial
    messages.append({
        "role": "assistant",
        "content": response.content[0].text
    })

    return response
```

## Mejores Prácticas de Caché

### 1. Cachear Contenido Grande y Reutilizado
✅ **Buenos candidatos para caché**:
- Documentación grande
- Instrucciones del sistema
- Ejemplos few-shot
- Definiciones de herramientas
- Bases de conocimiento
- Historial de conversación

❌ **Malos candidatos**:
- Prompts pequeños (< 1000 tokens)
- Contenido único, de una sola vez
- Contenido que cambia frecuentemente

### 2. Posicionar Contenido Cacheado Estratégicamente
```python
# ❌ Mal: Contenido variable al final del caché
system = [
    {
        "type": "text",
        "text": f"Large docs... User preferences: {user_prefs}",  # ¡Cambia por usuario!
        "cache_control": {"type": "ephemeral"}
    }
]

# ✅ Bien: Contenido estable en caché
system = [
    {
        "type": "text",
        "text": "Large docs...",  # Contenido estable
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": f"User preferences: {user_prefs}"  # Variable, no cacheado
    }
]
```

### 3. Cachear en Puntos de Ruptura (Breakpoints) Naturales
```python
system = [
    {
        "type": "text",
        "text": "Core instructions...",
    },
    {
        "type": "text",
        "text": "Documentation section 1...",
        "cache_control": {"type": "ephemeral"}  # Breakpoint 1
    },
    {
        "type": "text",
        "text": "Documentation section 2...",
        "cache_control": {"type": "ephemeral"}  # Breakpoint 2
    }
]
```

## Solución de Problemas

### El Caché No Se Usa
**Problema**: `cache_read_input_tokens` es siempre 0

**Soluciones**:
1. Comprueba el tamaño mínimo del caché (debe ser sustancial)
2. Verifica que la duración del caché no ha expirado (5 minutos)
3. Asegúrate de que se envía exactamente el mismo contenido
4. Confirma que `cache_control` está establecido correctamente

## Próximos Pasos
- Aprende sobre [Estrategias de Optimización de Caché](./06_cache_optimization.md)
- Explora [Técnicas de Reducción de Costes](./07_cost_reduction.md)
- Prueba [Procesamiento por Lotes](./08_batch_processing.md)

## Recursos Adicionales
- [Documentación Oficial de Caché de Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
