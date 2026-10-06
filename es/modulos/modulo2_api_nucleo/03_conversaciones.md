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
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=conversation_history
    )

    # 3. Obtener respuesta del asistente (une los bloques de texto; content también puede contener bloques de pensamiento)
    assistant_reply = "".join(b.text for b in response.content if b.type == "text")
    print(f"Claude: {assistant_reply}")

    # 4. Añadir respuesta del asistente al historial
    conversation_history.append({"role": "assistant", "content": assistant_reply})

# Ejemplo de uso
chat_turn("Hi, my name is Alex.")
chat_turn("What is my name?")
```

## Gestionando la Ventana de Contexto

Claude tiene una gran ventana de contexto (de 200K a 1M tokens según el modelo), pero no es infinita.

### Estrategias para Conversaciones Largas

1. **Truncamiento:** Eliminar los mensajes más antiguos cuando se alcanza el límite.
2. **Resumen:** Pedir a Claude que resuma la conversación hasta el momento, y reemplazar los mensajes antiguos con el resumen.
3. **Filtrado:** Eliminar mensajes menos importantes (ej. "Ok", "Gracias").

### Ejemplo: Truncamiento Simple

```python
MAX_HISTORY = 10  # Mantener los últimos 10 mensajes

def truncate(history, max_messages=MAX_HISTORY):
    """Conserva los últimos N mensajes; el prompt del sistema es un parámetro aparte, así que no le afecta."""
    trimmed = history[-max_messages:]
    # La lista debe empezar con un mensaje de usuario
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]
    return trimmed

conversation_history = truncate(conversation_history)
```

## Roles de Usuario vs. Asistente

- **User**: La entrada humana.
- **Assistant**: La salida de Claude.

**Reglas:**
- Los roles deben alternarse (Usuario -> Asistente -> Usuario).
- La lista debe empezar con un mensaje de `user`.

### Controlar el Formato de Salida (el Prefill Ya No Existe)
Los tutoriales antiguos "ponían palabras en boca de Claude" terminando la lista con un mensaje `assistant` (por ejemplo `{`). **Ese prefill devuelve un error 400 en los modelos actuales** (Fable 5.1, Opus 5.5, Sonnet 5.5 y la familia 4.6+). Usa en su lugar:

- **Salidas estructuradas**: restringe la respuesta a un esquema JSON con `output_config.format`.
- **Instrucciones claras** en el prompt de sistema ("Responde con un único objeto JSON y nada más").

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Describe un coche como JSON."}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "make": {"type": "string"},
                    "model": {"type": "string"},
                    "year": {"type": "integer"},
                },
                "required": ["make", "model", "year"],
                "additionalProperties": False,
            },
        }
    },
)
print(response.content[0].text)  # JSON válido que cumple el esquema (comprueba antes que stop_reason != "refusal")
```

Consulta la [documentación de salidas estructuradas](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) para el helper `client.messages.parse()`.

## Próximos Pasos
- Aprende sobre [Respuestas en Streaming](04_conceptos_basicos_streaming.md) para retroalimentación en tiempo real.
