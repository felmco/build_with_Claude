# 1.3 Entendiendo Solicitudes y Respuestas

La API de Claude usa una estructura basada en JSON para entradas y salidas. Entender esta estructura es clave para un desarrollo efectivo.

## El Objeto Message

Cuando llamas a `client.messages.create()`, estás creando un **Mensaje** (Message).

### Estructura de Solicitud (Entrada)

```python
{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "¡Hola, Claude!"}
    ]
}
```

**Campos Clave:**
- `model`: (Requerido) El ID del modelo a usar.
- `max_tokens`: (Requerido) La longitud máxima de salida.
- `messages`: (Requerido) Una lista de objetos de mensaje (`role` y `content`).
- `system`: (Opcional) Instrucciones a nivel de sistema.
- `temperature`: (Opcional) Controla la aleatoriedad (0.0 a 1.0).

### Estructura de Respuesta (Salida)

La API devuelve un objeto `Message`. Aquí se representa su estructura JSON:

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "¡Hola! ¿Cómo puedo ayudarte hoy?"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 9
  }
}
```

**Campos Clave:**
- `id`: Identificador único para la solicitud.
- `content`: Una lista de bloques de contenido. Usualmente contiene un bloque de texto.
- `role`: Siempre "assistant" para respuestas.
- `stop_reason`: Por qué se detuvo la generación.
  - `"end_turn"`: Completitud natural.
  - `"max_tokens"`: Alcanzó el límite.
- `usage`: Conteos de tokens para facturación.

## Accediendo a Datos de Respuesta en Python

El SDK de Python envuelve este JSON en un objeto.

```python
response = client.messages.create(...)

# Obtener el contenido de texto
text = response.content[0].text

# Obtener el ID
msg_id = response.id

# Obtener estadísticas de uso
input_tokens = response.usage.input_tokens
```

## Próximos Pasos
- Aprende cómo manejar problemas potenciales en [Manejo Básico de Errores](09_manejo_errores.md).
