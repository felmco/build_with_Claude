# Ejercicio 4: Gestión de Conversación

## 🎯 Objetivo
Mantén una lista de historial de mensajes para un chat coherente.

## ⏱️ Tiempo
30 minutos

## 📚 Requisitos Previos
- Listas en Python

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Parte 1: Lista de Historial
Crea una lista `messages = []`.

### Parte 2: Añadir (Appending)
Añade mensaje de usuario, envía a Claude, añade respuesta del asistente. Repite.

### Parte 3: Prompt del Sistema
Añade un prompt del sistema para dar una personalidad al asistente.

## 💻 Código de Inicio

```python
messages = []

while True:
    user_input = input("Tú: ")
    messages.append({"role": "user", "content": user_input})
    
    # TODO: Llamar API con `messages=messages`
    # TODO: Añadir respuesta a messages
```

## ✅ Salida Esperada

```
Una conversación donde Claude recuerda nombre/contexto.
```

## 🧪 Casos de Prueba

1. Mi nombre es Bob. 2. ¿Cuál es mi nombre?

## 🎁 Pistas

Mantén siempre el orden correcto de la lista.

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
response = client.messages.create(..., messages=messages)
messages.append({"role": "assistant", "content": response.content[0].text})
```
</details>

## 🚀 Extensiones

Implementa un comando 'limpiar' para reiniciar el historial.

## 📖 Resultados de Aprendizaje

- ✅ Modelos mentales de contexto
- ✅ Gestión de estado

## 🔗 Lecciones Relacionadas
- [Conversaciones](../../modulos/modulo2_api_nucleo/03_conversaciones.md)

## ❓ Problemas Comunes

Límite de longitud de contexto excedido (necesita lógica de truncamiento).

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
