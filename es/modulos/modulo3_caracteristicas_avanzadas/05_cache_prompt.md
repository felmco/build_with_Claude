# 3.2 Entendiendo el Almacenamiento en Caché de Prompts

## Introducción
El almacenamiento en caché de prompts permite reutilizar grandes porciones de tu prompt a través de múltiples peticiones, reduciendo drásticamente los costes (las lecturas de caché cuestan cerca del 10% del precio normal de entrada) y la latencia para contenido repetido.

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
Petición 1: Procesa 10,000 tokens → Cachéalos → Coste total + 25% de recargo por escritura
Petición 2: Lee de caché → ¡90% reducción de coste!
Petición 3: Lee de caché → ¡90% reducción de coste!
```

## Comparación de Costes

### Precios (multiplicadores del precio base de entrada)
- **Escritura en caché (TTL de 5 minutos)**: 1.25x el precio base de entrada
- **Escritura en caché (TTL de 1 hora)**: 2x el precio base de entrada
- **Lectura de caché**: aproximadamente 0.1x el precio base de entrada (incluso menos en algunos modelos, por ejemplo 0.05x en Claude Opus 5.5)

Los precios cambian, así que consulta la [página de precios](https://claude.com/pricing). El ejemplo siguiente usa Claude Sonnet 5.5 a $2 por millón de tokens de entrada: $2.50 por MTok para una escritura de caché de 5 minutos y $0.20 por MTok para una lectura de caché.

### Ejemplo de Cálculo
Prompt de 10,000 tokens, usado 100 veces (dentro de la vida del caché):

**Sin caché**:
```
100 peticiones × 10,000 tokens × $2/MTok = $2.00
```

**Con caché**:
```
Escritura: 1 × 10,000 × $2.50/MTok = $0.025
Lecturas: 99 × 10,000 × $0.20/MTok = $0.198
Total: $0.025 + $0.198 = $0.223
Ahorro: $2.00 - $0.223 = $1.777 (aproximadamente 89% de reducción)
```

Como una escritura cuesta 1.25x y una lectura 0.1x, el caché se amortiza con tan solo dos peticiones que compartan el prefijo.

## Cómo Funciona el Caché de Prompts

### Puntos de Ruptura de Caché (Breakpoints)
Marca el contenido a ser cacheado usando `cache_control`:

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
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
- **Duración por defecto**: 5 minutos (`{"type": "ephemeral"}`)
- **Actualización**: Cada acierto de caché (hit) reinicia el temporizador sin coste adicional, así que un prefijo que se usa al menos cada 5 minutos se mantiene caliente
- **Opción de 1 hora**: `{"type": "ephemeral", "ttl": "1h"}` cuesta más de escribir (2x) pero sobrevive a pausas más largas entre peticiones
- **Límites**: como máximo 4 puntos de ruptura `cache_control` por petición. Los cachés están limitados a tu workspace y al modelo.
- **Tamaño mínimo**: el prefijo debe alcanzar un mínimo que depende del modelo (de 512 a 4096 tokens, ver Solución de Problemas) o simplemente no se cachea, sin avisar.

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

[... imagine this is several thousand tokens of documentation ...]
"""

def ask_with_caching(question: str):
    """Preguntar con base de conocimiento cacheada"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
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

    return next(b.text for b in response.content if b.type == "text")

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

**Salida Esperada**:
```
Petición #1: What are Python data types?
📊 Uso de Tokens:
   Tokens entrada: 150
   Creación caché: 2500  ← Caché creado (primera vez)
   Lectura caché: 0
   Tokens salida: 120

Petición #2: Explain Python functions
📊 Uso de Tokens:
   Tokens entrada: 150
   Creación caché: 0
   Lectura caché: 2500  ← ¡Leído del caché! (90% de ahorro)
   Tokens salida: 115
```

## Cacheando Prompts del Sistema

### Prompt del Sistema Único
```python
message = client.messages.create(
    model="claude-sonnet-5-5",
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
    model="claude-sonnet-5-5",
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

Pon un punto de ruptura en el último bloque del turno más reciente. Cada nueva petición lee entonces toda la conversación anterior desde el caché. (Si no necesitas controlar la colocación, puedes pasar en su lugar un `cache_control={"type": "ephemeral"}` de nivel superior a `messages.create()`, que coloca el punto de ruptura automáticamente en el último bloque cacheable.)

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
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=cached_messages
    )

    # Añadir respuesta del asistente al historial (solo texto; en bucles de uso
    # de herramientas añade response.content sin cambios para conservar los bloques thinking)
    messages.append({
        "role": "assistant",
        "content": next(b.text for b in response.content if b.type == "text")
    })

    return response
```

## Cacheando con Herramientas

**tools_with_caching.py**:
```python
#!/usr/bin/env python3
"""Caché con definiciones de herramientas"""

from anthropic import Anthropic

client = Anthropic()

# Definiciones de herramientas grandes (¡cachéalas!)
TOOLS = [
    {
        "name": "search_database",
        "description": "Searches a large database with complex query capabilities...",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "filters": {"type": "object", "description": "Filter criteria"},
                "limit": {"type": "integer", "description": "Result limit"}
            },
            "required": ["query"]
        }
    },
    # ... imagina 50 definiciones de herramientas más ...
]

def query_with_tools_cached(question: str):
    """Consultar con definiciones de herramientas cacheadas"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        tools=TOOLS,
        system=[
            {
                "type": "text",
                "text": "You are a helpful assistant with access to various tools.",
                "cache_control": {"type": "ephemeral"}  # Cachear sistema + herramientas
            }
        ],
        messages=[
            {"role": "user", "content": question}
        ]
    )

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
- Prompts por debajo del tamaño mínimo cacheable del modelo (de 512 a 4096 tokens según el modelo)
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

### 4. Monitorizar el Rendimiento del Caché
```python
def monitor_cache_usage(response):
    """Monitorizar tasa de aciertos de caché y ahorros"""
    usage = response.usage

    cache_creation = getattr(usage, 'cache_creation_input_tokens', 0)
    cache_read = getattr(usage, 'cache_read_input_tokens', 0)
    input_tokens = usage.input_tokens

    if cache_read > 0:
        # ¡Acierto de caché!
        savings_percent = (cache_read / (cache_read + input_tokens)) * 100
        print(f"✅ ¡Acierto de caché! {savings_percent:.1f}% de la entrada viene del caché")
    elif cache_creation > 0:
        # Caché creado
        print(f"📝 Caché creado: {cache_creation} tokens")
    else:
        # Sin caché
        print("❌ No se usó caché")

    return {
        "cache_creation": cache_creation,
        "cache_read": cache_read,
        "input_tokens": input_tokens,
        "cache_hit_rate": cache_read / (cache_read + input_tokens) if cache_read > 0 else 0
    }
```

## Avanzado: Caché Multinivel

```python
#!/usr/bin/env python3
"""Estrategia de caché multinivel"""

from anthropic import Anthropic

client = Anthropic()

def multi_level_cache(project_id: str, user_query: str):
    """
    Nivel 1: Documentación global (caché para todos los usuarios)
    Nivel 2: Contexto específico del proyecto (caché por proyecto)
    Nivel 3: Datos específicos del usuario (sin caché, cambian con frecuencia)
    """

    # Nivel 1: Global (cambia con menos frecuencia)
    global_docs = "Global API documentation..."

    # Nivel 2: Específico del proyecto (cambia por proyecto)
    project_context = f"Project {project_id} specific information..."

    # Nivel 3: Específico del usuario (cambia en cada petición)
    user_context = f"Current query: {user_query}"

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": global_docs,
                "cache_control": {"type": "ephemeral"}  # Caché nivel 1
            },
            {
                "type": "text",
                "text": project_context,
                "cache_control": {"type": "ephemeral"}  # Caché nivel 2
            },
            {
                "type": "text",
                "text": "You are a helpful assistant."  # Sin caché
            }
        ],
        messages=[
            {"role": "user", "content": user_context}  # Sin caché
        ]
    )

    return response
```

## Cacheando con Imágenes

```python
import base64

# Cachear datos de imagen para análisis repetido
with open("diagram.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    },
                    "cache_control": {"type": "ephemeral"}  # Cachear imagen
                },
                {
                    "type": "text",
                    "text": "Analyze this diagram"
                }
            ]
        }
    ]
)
```

## Ejemplo del Mundo Real: RAG con Caché

**rag_with_caching.py**:
```python
#!/usr/bin/env python3
"""RAG (Retrieval Augmented Generation) con caché"""

from anthropic import Anthropic
from typing import List

client = Anthropic()

class CachedRAG:
    """Sistema RAG con caché de prompts"""

    def __init__(self, knowledge_base: str):
        self.knowledge_base = knowledge_base
        self.client = Anthropic()

    def query(self, question: str, context_docs: List[str] = None):
        """
        Consultar con base de conocimiento cacheada y contexto nuevo opcional
        """
        system_parts = [
            {
                "type": "text",
                "text": "You are a helpful assistant. Answer questions based on the provided knowledge base."
            },
            {
                "type": "text",
                "text": f"Knowledge Base:\n{self.knowledge_base}",
                "cache_control": {"type": "ephemeral"}  # Cachear la base principal
            }
        ]

        # Añadir documentos de contexto nuevos (sin caché)
        if context_docs:
            context_text = "\n\n".join(context_docs)
            system_parts.append({
                "type": "text",
                "text": f"Additional Context:\n{context_text}"
            })

        response = self.client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            system=system_parts,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        return next(b.text for b in response.content if b.type == "text")

def main():
    """Probar RAG con caché"""

    # Base de conocimiento grande (cacheada)
    kb = """
    Product Documentation:
    - Product A: Features, pricing, specifications...
    - Product B: Features, pricing, specifications...
    [... imagine 10,000 tokens of documentation ...]
    """

    rag = CachedRAG(kb)

    # Primera consulta - crea el caché
    print("Consulta 1:")
    answer1 = rag.query("What are the features of Product A?")
    print(answer1)

    # Segunda consulta - usa el caché
    print("\nConsulta 2:")
    answer2 = rag.query("How much does Product B cost?")
    print(answer2)

    # Consulta con contexto adicional
    print("\nConsulta 3 con contexto nuevo:")
    fresh_context = ["Product A is currently on sale for 20% off"]
    answer3 = rag.query("Is Product A on sale?", context_docs=fresh_context)
    print(answer3)

if __name__ == "__main__":
    main()
```

## Solución de Problemas

### El Caché No Se Usa
**Problema**: `cache_read_input_tokens` es siempre 0

**Soluciones**:
1. Comprueba el prefijo mínimo cacheable. Depende del modelo: 512 tokens en Claude Sonnet 5.5, Opus 5.5 y Fable 5.1; 1024 en varios modelos Sonnet/Opus anteriores; 4096 en Claude Haiku 4.5. Los prefijos más cortos simplemente no se cachean (sin error, `cache_creation_input_tokens` es 0). Confirma el valor vigente en la documentación.
2. Verifica que el caché no ha expirado (5 minutos por defecto, medidos desde el inicio de la última petición que lo escribió o leyó)
3. Asegúrate de que el prefijo es idéntico byte a byte. El caché es una coincidencia de prefijo en el orden herramientas, sistema, mensajes, así que una marca de tiempo, una lista de herramientas modificada o claves JSON sin ordenar al principio del prompt invalidan todo lo que viene después.
4. Confirma que `cache_control` está en el último bloque del prefijo estable, y que usas el mismo modelo y workspace

### Altos Costes de Creación de Caché
**Problema**: Se crean demasiados cachés

**Soluciones**:
1. Consolida el contenido cacheable
2. Usa menos puntos de ruptura de caché
3. Cachea solo contenido que se reutiliza con frecuencia
4. Asegúrate de que el prefijo es estable, para que las entradas se lean en lugar de reescribirse

## Referencia Rápida

```python
# Cachear prompt del sistema
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Large content to cache...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Question"}]
)

# Comprobar uso de caché
usage = message.usage
print(f"Caché creado: {usage.cache_creation_input_tokens}")
print(f"Caché leído: {usage.cache_read_input_tokens}")
```

## Próximos Pasos
- Aprende sobre [Estrategias de Optimización de Caché](06_optimizacion_cache.md)
- Explora [Técnicas de Reducción de Costes](07_reduccion_costos.md)
- Prueba [Procesamiento por Lotes](08_procesamiento_lotes.md)

## Recursos Adicionales
- [Documentación Oficial de Caché de Prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anuncio del Caché de Prompts](https://www.anthropic.com/news/prompt-caching)
- [Mejores Prácticas de Caché](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#best-practices)
