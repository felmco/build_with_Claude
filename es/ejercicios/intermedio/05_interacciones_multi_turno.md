# Ejercicio 5: Lógica Multi-turno

## 🎯 Objetivo
Crea un juego de '20 Preguntas' con Claude.

## ⏱️ Tiempo
45 minutos

## 📚 Requisitos Previos
- Gestión de Conversación

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Objetivo
Guioniza un flujo específico:
1. Claude elige un objeto (puedes indicarlo en el prompt del sistema).
2. El usuario hace preguntas de sí/no.
3. Claude responde.
4. Termina cuando el usuario adivina correctamente.

## 💻 Código de Inicio

```python
system_prompt = "Estás organizando un juego de 20 preguntas. Elige un objeto (una tostadora) y responde preguntas de sí/no."

```

## ✅ Salida Esperada

```
Flujo de juego interactivo.
```

## 🧪 Casos de Prueba

Jugar el juego.

## 🎁 Pistas

Usa prompt del sistema para imponer reglas.

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
import anthropic

client = anthropic.Anthropic()
system_prompt = (
    "Estás organizando un juego de 20 preguntas. Elige en secreto un objeto (una tostadora). "
    "Responde a cada pregunta solo con 'Sí', 'No' o 'A veces'. Nunca reveles el objeto "
    "a menos que el jugador lo adivine o haya usado las 20 preguntas. Lleva la cuenta de las preguntas."
)
messages = []

while True:
    user_input = input("Tú: ")
    if user_input.lower() in ("salir", "exit"):
        break
    messages.append({"role": "user", "content": user_input})
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        system=system_prompt,
        messages=messages,
    )
    reply = "".join(b.text for b in response.content if b.type == "text")
    messages.append({"role": "assistant", "content": reply})
    print(f"Claude: {reply}")
```

Nota: el objeto secreto vive solo en el prompt del sistema, así que el jugador nunca lo ve. Para tener un objeto distinto en cada partida, elige uno en tu propio código e insértalo en el prompt.
</details>

## 🚀 Extensiones

Haz que Claude adivine TU objeto.

## 📖 Resultados de Aprendizaje

- ✅ Conversaciones guiadas
- ✅ Adherencia a instrucciones del sistema

## 🔗 Lecciones Relacionadas
- [Prompts del Sistema](../../modulos/modulo2_api_nucleo/02_prompts_sistema.md)

## ❓ Problemas Comunes

Claude revela la respuesta demasiado pronto.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
