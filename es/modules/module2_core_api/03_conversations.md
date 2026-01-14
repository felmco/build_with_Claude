# 2.1 Gestionando Conversaciones

La API de Mensajes no tiene estado (stateless), lo que significa que Claude no "recuerda" peticiones pasadas automáticamente. Debes gestionar el historial de conversación tú mismo.

## Cómo Funciona el Contexto

Para tener una conversación de múltiples turnos, añades cada nuevo mensaje a una lista y envías la lista *entera* de vuelta a la API con cada nueva petición.

### El Bucle de Conversación

```python
import anthropic

client = anthropic.Anthropic()
conversation_history = []

def chat_turn(user_input):
    # 1. Añadir mensaje de usuario al historial
    conversation_history.append({"role": "user", "content": user_input})

    # 2. Enviar historial a la API
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=conversation_history
    )

    # 3. Obtener respuesta del asistente
    assistant_reply = response.content[0].text
    print(f"Claude: {assistant_reply}")

    # 4. Añadir respuesta del asistente al historial
    conversation_history.append({"role": "assistant", "content": assistant_reply})

# Ejemplo de uso
chat_turn("Hi, my name is Alex.")
chat_turn("What is my name?")
```

## Gestionando la Ventana de Contexto

Claude tiene una gran ventana de contexto (200K tokens), pero no es infinita.

### Estrategias para Conversaciones Largas

1. **Truncamiento:** Eliminar los mensajes más antiguos cuando se alcanza el límite.
2. **Resumen:** Pedir a Claude que resuma la conversación hasta el momento, y reemplazar los mensajes antiguos con el resumen.
3. **Filtrado:** Eliminar mensajes menos importantes (ej. "Ok", "Gracias").

### Ejemplo: Truncamiento Simple

```python
MAX_HISTORY = 10  # Mantener los últimos 10 mensajes

if len(conversation_history) > MAX_HISTORY:
    # ¿Mantener el prompt del sistema o el primer mensaje si es crucial?
    # Aquí simplemente cortamos los últimos N mensajes
    conversation_history = conversation_history[-MAX_HISTORY:]
```

## Roles de Usuario vs. Asistente

- **User**: La entrada humana.
- **Assistant**: La salida de Claude.

**Reglas:**
- Los roles deben alternarse (Usuario -> Asistente -> Usuario).
- La lista debe empezar con un mensaje de `user`.

### Pre-rellenar la Respuesta del Asistente
Puedes "poner palabras en la boca de Claude" añadiendo un mensaje `assistant` como el último mensaje en la lista *sin* un mensaje de usuario correspondiente siguiéndolo. Esto es útil para:
- Forzar un formato específico (ej. `{`).
- Guiar el tono.

*Nota: Esta característica se maneja de forma diferente en la API. Suministras el pre-relleno como el último mensaje con rol `assistant`.*

```python
messages = [
    {"role": "user", "content": "Write a JSON object describing a car."},
    {"role": "assistant", "content": "{"} # Pre-relleno
]

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
# Claude continúa desde "{":  "make": "Toyota", ...
```

## Próximos Pasos
- Aprende sobre [Respuestas en Streaming](./04_streaming_basics.md) para retroalimentación en tiempo real.
