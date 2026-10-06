# Ejercicio 1: Hola Claude

## 🎯 Objetivo
Haz tu primera llamada a la API de Claude y muestra una respuesta formateada.

## ⏱️ Tiempo
15 minutos

## 📚 Requisitos Previos
- Python 3.10+ instalado
- SDK de Anthropic instalado
- Clave API configurada
- Completado [Módulo 1: Primera Llamada a la API](../../modulos/modulo1_fundamentos/07_primera_llamada_api.md)

## 🎓 Nivel de Dificultad
⭐ Principiante

## 📝 Instrucciones

### Parte 1: Hola Básico
Crea un script que envíe "Hola, Claude!" e imprima la respuesta.

**Requisitos**:
- Inicializar cliente Anthropic
- Enviar un mensaje simple
- Imprimir la respuesta
- Incluir manejo de errores básico

### Parte 2: Salida Formateada
Mejora tu script para mostrar:
- Un encabezado
- La pregunta del usuario
- La respuesta de Claude
- Información de uso de tokens

### Parte 3: Múltiples Preguntas
Haz a Claude tres preguntas diferentes y muestra todas las respuestas bien formateadas.

## 💻 Código de Inicio

```python
#!/usr/bin/env python3
"""Ejercicio 1: Hola Claude"""

from anthropic import Anthropic

def main():
    # TODO: Inicializar el cliente

    # TODO: Enviar un mensaje a Claude

    # TODO: Imprimir la respuesta

    pass

if __name__ == "__main__":
    main()
```

## ✅ Salida Esperada

```
═══════════════════════════════════════
Ejercicio 1: Hola Claude
═══════════════════════════════════════

Tú: Hola, Claude!

Claude: ¡Hola! Soy Claude, un asistente de IA creado por Anthropic.
¿Cómo puedo ayudarte hoy?

📊 Uso:
   Tokens de entrada: 12
   Tokens de salida: 25
   Tokens totales: 37
```

## 🧪 Casos de Prueba

1. **Prueba 1**: Saludo básico
   - Entrada: "Hola, Claude!"
   - Esperado: Respuesta de saludo amigable

2. **Prueba 2**: Pregunta
   - Entrada: "¿Cuánto es 2 + 2?"
   - Esperado: "4" o "2 + 2 es igual a 4"

3. **Prueba 3**: Petición creativa
   - Entrada: "Cuéntame un chiste de una frase"
   - Esperado: Un chiste corto

## 🎁 Pistas

<details>
<summary>Pista 1: Inicializando el cliente</summary>

```python
from anthropic import Anthropic
client = Anthropic()  # Usa var de entorno ANTHROPIC_API_KEY
```
</details>

<details>
<summary>Pista 2: Haciendo una llamada a la API</summary>

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Tu mensaje aquí"}
    ]
)
```
</details>

<details>
<summary>Pista 3: Accediendo a la respuesta</summary>

```python
response_text = message.content[0].text
print(response_text)
```
</details>

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
#!/usr/bin/env python3
"""Ejercicio 1: Hola Claude - Solución"""

import os

import anthropic
from anthropic import Anthropic

def send_message(client, user_message: str):
    """Enviar un mensaje a Claude y devolver respuesta"""
    try:
        return client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
    except anthropic.APIError as e:
        print(f"❌ Error de API: {e}")
        return None

def display_response(user_message: str, message):
    """Mostrar respuesta formateada"""
    if message is None:
        return
    # Unir los bloques de texto (en algunos modelos content también puede incluir bloques que no son de texto)
    text = "".join(b.text for b in message.content if b.type == "text")
    print(f"\nTú: {user_message}\n")
    print(f"Claude: {text}\n")
    print("📊 Uso:")
    print(f"   Tokens de entrada: {message.usage.input_tokens}")
    print(f"   Tokens de salida: {message.usage.output_tokens}")
    print(f"   Tokens totales: {message.usage.input_tokens + message.usage.output_tokens}")

def main():
    """Función principal"""
    # Encabezado
    print("═" * 60)
    print("Ejercicio 1: Hola Claude")
    print("═" * 60)

    # Comprobar clave API
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Por favor establece la variable de entorno ANTHROPIC_API_KEY")
        return

    # Inicializar cliente
    client = Anthropic()

    # Parte 1: Hola Básico
    user_message = "Hola, Claude!"
    message = send_message(client, user_message)
    display_response(user_message, message)

    # Parte 3: Múltiples preguntas
    questions = [
        "¿Cuánto es 2 + 2?",
        "Cuéntame un chiste de una frase",
        "¿Cuál es la capital de Francia?"
    ]

    print("\n" + "═" * 60)
    print("Múltiples Preguntas")
    print("═" * 60)

    for question in questions:
        message = send_message(client, question)
        display_response(question, message)
        print("-" * 60)

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensiones

Una vez hayas completado el ejercicio básico, intenta estas extensiones:

### Extensión 1: Modo Interactivo
Haz el script interactivo - sigue pidiendo entrada al usuario hasta que escriba 'salir'

```python
while True:
    user_input = input("\nTú: ")
    if user_input.lower() == 'salir':
        break
    # Enviar a Claude y mostrar respuesta
```

### Extensión 2: Guardar Conversación
Guarda la conversación en un archivo de texto

### Extensión 3: Añadir Colores
Usa la librería `colorama` para añadir colores a la salida

### Extensión 4: Cronometrar las Respuestas
Mide y muestra cuánto tiempo tarda cada respuesta

### Extensión 5: Comparar Modelos
Envía la misma pregunta a diferentes modelos (Haiku, Sonnet, Opus) y compara

## 📖 Resultados de Aprendizaje

Después de completar este ejercicio, deberías entender:
- ✅ Cómo inicializar el cliente Anthropic
- ✅ Cómo hacer una llamada básica a la API
- ✅ Cómo acceder al contenido de la respuesta
- ✅ Cómo comprobar el uso de tokens
- ✅ Manejo de errores básico

## 🔗 Lecciones Relacionadas
- [Primera Llamada a la API](../../modulos/modulo1_fundamentos/07_primera_llamada_api.md)
- [Petición y Respuesta](../../modulos/modulo1_fundamentos/08_solicitud_respuesta.md)
- [API de Mensajes](../../modulos/modulo2_api_nucleo/01_api_mensajes.md)

## ❓ Problemas Comunes

### Problema 1: Clave API No Encontrada
**Error**: `ANTHROPIC_API_KEY not found`

**Solución**:
```bash
export ANTHROPIC_API_KEY='tu-clave-api'
```

### Problema 2: Módulo No Encontrado
**Error**: `ModuleNotFoundError: No module named 'anthropic'`

**Solución**:
```bash
pip install anthropic
```

### Problema 3: Error de Atributo
**Error**: `AttributeError: 'Message' object has no attribute 'content'`

**Solución**: Asegúrate de que estás accediendo a `message.content[0].text`, no solo a `message.content`

## 🎉 Finalización

¡Felicidades! Has completado tu primer ejercicio. Avanza al [Ejercicio 2: Chatbot Simple](02_chatbot_simple.md)

---

**¿Necesitas ayuda?** Revisa [Módulo 1: Primera Llamada a la API](../../modulos/modulo1_fundamentos/07_primera_llamada_api.md)
