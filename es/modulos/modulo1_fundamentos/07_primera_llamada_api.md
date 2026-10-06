# 1.4 Tu Primera Llamada a la API

## Introducción
Esta guía te acompaña en la realización de tu primera llamada a la API de Claude. ¡Al final, habrás enviado un mensaje a Claude y recibido una respuesta!

## Requisitos Previos
- ✅ Python 3.10+ instalado
- ✅ SDK de Anthropic instalado (`pip install anthropic`)
- ✅ Clave API configurada (ver [Gestión de Claves API](06_claves_api.md))

## El Ejemplo Más Simple Posible

**hello_claude.py**:
```python
from anthropic import Anthropic

# Inicializar el cliente
client = Anthropic()  # Usa la variable de entorno ANTHROPIC_API_KEY

# Haz tu primera llamada a la API
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude! Introduce yourself in one sentence."}
    ]
)

# Imprimir la respuesta
print(message.content[0].text)
```

Ejecútalo:
```bash
python hello_claude.py
```

**Salida Esperada**:
```
I'm Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest.
```

🎉 ¡Felicidades! ¡Acabas de hacer tu primera llamada a la API de Claude!

> **Nota:** `message.content[0].text` es la forma abreviada que se usa en todo el curso. Funciona para respuestas de texto simple, pero `content` también puede empezar con un bloque `thinking` (Opus 5.5 y Fable 5.1 siempre piensan) o estar vacío cuando `stop_reason` es `"refusal"`. En código de producción, elige el bloque de texto: `next(b.text for b in message.content if b.type == "text")`.

## Entendiendo el Código

Vamos a desglosar cada parte:

### 1. Importar e Inicializar

```python
from anthropic import Anthropic

client = Anthropic()  # Usa automáticamente la variable de entorno ANTHROPIC_API_KEY
```

El cliente `Anthropic()`:
- Busca la variable de entorno `ANTHROPIC_API_KEY`
- Configura la autenticación
- Proporciona métodos para interactuar con la API

### 2. Crear un Mensaje

```python
message = client.messages.create(
    model="claude-sonnet-5-5",  # Qué modelo usar
    max_tokens=1024,                      # Longitud máxima de respuesta
    messages=[                            # Historial de conversación
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
```

**Parámetros explicados**:
- `model`: Qué modelo de Claude usar (Sonnet 5.5 recomendado)
- `max_tokens`: Tokens máximos en la respuesta (1 token ≈ 0.75 palabras)
- `messages`: Lista de mensajes en la conversación

### 3. Acceder a la Respuesta

```python
print(message.content[0].text)
```

La respuesta es un objeto `Message` con:
- `content`: Lista de bloques de contenido
- `content[0].text`: El texto real de la respuesta
- `usage`: Información de uso de tokens
- `model`: Modelo que generó la respuesta

## Ejemplo Completo con Manejo de Errores

**robust_example.py**:
```python
#!/usr/bin/env python3
"""Un primer ejemplo robusto de llamada a la API con manejo de errores"""

import os
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError

def make_api_call():
    """Hacer una llamada a la API de Claude con manejo de errores"""

    # Comprobar si la clave API está configurada
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: Variable de entorno ANTHROPIC_API_KEY no establecida")
        print("Establécela usando: export ANTHROPIC_API_KEY='tu-clave-api'")
        return

    try:
        # Inicializar cliente
        print("🔄 Inicializando cliente...")
        client = Anthropic()

        # Hacer llamada a la API
        print("📤 Enviando mensaje a Claude...")
        message = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude! Introduce yourself in one sentence."
                }
            ]
        )

        # Mostrar respuesta
        print("\n✅ ¡Respuesta recibida!")
        print("─" * 50)
        print(message.content[0].text)
        print("─" * 50)

        # Mostrar información de uso
        print(f"\n📊 Uso:")
        print(f"   Tokens de entrada: {message.usage.input_tokens}")
        print(f"   Tokens de salida: {message.usage.output_tokens}")
        print(f"   Tokens totales: {message.usage.input_tokens + message.usage.output_tokens}")

    except RateLimitError as e:
        print(f"❌ Límite de velocidad excedido: {e}")
        print("   Inténtalo de nuevo en unos momentos")

    except APIConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        print("   Comprueba tu conexión a internet")

    except APIError as e:
        print(f"❌ Error de API: {e}")
        print("   Comprueba el estado de la API: https://status.anthropic.com")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    make_api_call()
```

## Ejemplo Interactivo

Crea un script interactivo que tome la entrada del usuario:

**interactive_claude.py**:
```python
#!/usr/bin/env python3
"""Conversación interactiva con Claude"""

import os
from anthropic import Anthropic

def main():
    """Ejecutar conversación interactiva con Claude"""

    # Comprobar clave API
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Por favor establece la variable de entorno ANTHROPIC_API_KEY")
        return

    client = Anthropic()

    print("Chat Interactivo con Claude")
    print("Escribe 'quit' para salir\n")
    print("─" * 50)

    while True:
        # Obtener entrada del usuario
        user_input = input("\nTú: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("¡Adiós!")
            break

        if not user_input:
            continue

        try:
            # Hacer llamada a la API
            message = client.messages.create(
                model="claude-sonnet-5-5",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            # Mostrar respuesta
            print(f"\nClaude: {message.content[0].text}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

Ejecútalo:
```bash
python interactive_claude.py
```

Interacción de ejemplo:
```
Chat Interactivo con Claude
Escribe 'quit' para salir
──────────────────────────────────────────────────

Tú: What's 25 * 4?

Claude: 25 * 4 = 100

Tú: Explain how photosynthesis works

Claude: Photosynthesis is the process by which plants convert light energy...

Tú: quit
¡Adiós!
```

## Entendiendo la Estructura de la Respuesta

El objeto `Message` contiene varios campos importantes:

```python
message = client.messages.create(...)

# Texto de respuesta principal
text = message.content[0].text

# Metadatos del mensaje
message_id = message.id              # ID único del mensaje
model_used = message.model           # Modelo que generó la respuesta
role = message.role                  # Siempre "assistant"

# Uso de tokens
input_tokens = message.usage.input_tokens
output_tokens = message.usage.output_tokens

# Razón de parada
stop_reason = message.stop_reason  # Por qué paró la generación

print(f"ID Mensaje: {message_id}")
print(f"Modelo: {model_used}")
print(f"Tokens entrada: {input_tokens}")
print(f"Tokens salida: {output_tokens}")
print(f"Razón parada: {stop_reason}")
print(f"\nRespuesta:\n{text}")
```

**Salida**:
```
ID Mensaje: msg_01ABC123XYZ...
Modelo: claude-sonnet-5-5
Tokens entrada: 15
Tokens salida: 25
Razón parada: end_turn

Respuesta:
I'm Claude, an AI assistant created by Anthropic.
```

## Parámetros Comunes

### max_tokens
Controla la longitud máxima de la respuesta:

```python
# Respuesta corta
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=50,  # Muy corta
    messages=[{"role": "user", "content": "Write a story"}]
)

# Respuesta larga
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,  # Mucho más larga
    messages=[{"role": "user", "content": "Write a detailed story"}]
)
```

**Directrices**:
- Mínimo: 1 token
- Máximo: hasta 128K tokens en los modelos actuales (64K en Haiku 4.5); específico del modelo
- Usa streaming para valores grandes (aproximadamente por encima de 16K) para que la petición no agote el tiempo de espera
- 1 token ≈ 0.75 palabras en inglés
- Establecer basado en la longitud de respuesta esperada

### temperature
Controla la aleatoriedad (0.0 a 1.0).

> ⚠️ **Modelos actuales:** Claude Fable 5.1, Opus 5.5 y Sonnet 5.5 rechazan `temperature`/`top_p`/`top_k` no predeterminados con un 400. Allí usa el prompt y `effort`. Los ejemplos siguientes usan **Claude Haiku 4.5** y modelos anteriores.

```python
# Más enfocado y determinista
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=0.0,  # Más determinista
    messages=[{"role": "user", "content": "What is 2+2?"}]
)

# Más creativo y variado
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    temperature=1.0,  # Más creativo
    messages=[{"role": "user", "content": "Write a creative story"}]
)
```

**Directrices**:
- 0.0: Determinista, respuestas consistentes
- 0.5-0.7: Equilibrado (predeterminado: 1.0)
- 1.0: Más creativo, respuestas variadas
- Usa temperatura baja para tareas factuales
- Usa temperatura alta para tareas creativas

### system
Proporcionar instrucciones a Claude:

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    system="You are a helpful Python tutor. Explain concepts simply with examples.",
    messages=[
        {"role": "user", "content": "What are list comprehensions?"}
    ]
)
```

## Probando Diferentes Modelos

**model_comparison.py**:
```python
from anthropic import Anthropic

client = Anthropic()
prompt = "Explain quantum computing in one sentence."

models = {
    "Haiku 4.5": "claude-haiku-4-5",
    "Sonnet 5.5": "claude-sonnet-5-5",
    "Opus 5.5": "claude-opus-5-5"
}

print("Comparing Models")
print("=" * 60)

for name, model_id in models.items():
    print(f"\n{name}:")
    print("-" * 60)

    message = client.messages.create(
        model=model_id,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    print(message.content[0].text)
    print(f"Tokens: {message.usage.output_tokens}")
```

## Poniéndolo Todo Junto: Plantilla Completa

**claude_template.py**:
```python
#!/usr/bin/env python3
"""Plantilla completa para llamadas a la API de Claude"""

import os
import sys
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def validate_environment():
    """Validar variables de entorno requeridas"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY no establecida")
        sys.exit(1)

def create_client():
    """Crear y devolver cliente Anthropic"""
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def send_message(client, prompt: str, system: str = None):
    """Enviar un mensaje a Claude y devolver respuesta"""
    try:
        params = {
            "model": "claude-sonnet-5-5",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)
        return message.content[0].text

    except APIError as e:
        print(f"Error de API: {e}")
        return None

def main():
    """Función principal"""
    validate_environment()
    client = create_client()

    # Ejemplo de uso
    response = send_message(
        client,
        prompt="What is the capital of France?",
        system="You are a geography expert. Be concise."
    )

    if response:
        print(f"Respuesta: {response}")

if __name__ == "__main__":
    main()
```

## Problemas Comunes Primera Vez

### Problema 1: Clave API No Encontrada
```
Error: ANTHROPIC_API_KEY not set
```
**Solución**: Establecer variable de entorno:
```bash
export ANTHROPIC_API_KEY='tu-clave-aqui'
```

### Problema 2: Error de Importación
```
ModuleNotFoundError: No module named 'anthropic'
```
**Solución**: Instalar SDK:
```bash
pip install anthropic
```

### Problema 3: Clave API Inválida
```
AuthenticationError: Invalid API key
```
**Solución**: Comprueba tu clave API:
- Verifica que empieza con `sk-ant-api`
- Comprueba espacios extra o comillas
- Regenera la clave en la consola si es necesario

### Problema 4: Límite de Velocidad (Rate Limiting)
```
RateLimitError: 429 Too Many Requests
```
**Solución**: Añadir lógica de reintento o ralentizar peticiones

## Referencia Rápida

```python
# Ejemplo mínimo
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

## Próximos Pasos
- Aprende sobre [Manejo de Peticiones y Respuestas](08_solicitud_respuesta.md)
- Explora [Manejo de Errores](09_manejo_errores.md)
- Prueba [Módulo 2: Características Principales de la API](../modulo2_api_nucleo/README.md)

## Ejercicios de Práctica

1. **Hola Mundo**: Haz una llamada simple a la API
2. **Calculadora**: Pide a Claude que resuelva problemas matemáticos
3. **Traductor**: Traduce texto entre idiomas
4. **Ayudante de Código**: Pide ayuda de programación
5. **Escritura Creativa**: Genera una historia corta

¡Prueba estos por tu cuenta para practicar!

## Recursos Adicionales
- [Referencia Oficial de API](https://platform.claude.com/docs/en/api/messages)
- [Documentación SDK Python](https://github.com/anthropics/anthropic-sdk-python)
- [Repositorio de Código de Ejemplo](https://github.com/anthropics/anthropic-quickstarts)
