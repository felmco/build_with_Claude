# Ejercicio 5: Experimentos de Temperatura

## 🎯 Objetivo
Observa cómo el parámetro 'temperature' afecta la aleatoriedad de la salida.

## ⏱️ Tiempo
15 minutos

## 📚 Requisitos Previos
Ninguno

## 🎓 Nivel de Dificultad
⭐ Principiante

## 📝 Instrucciones

### Parte 1: Determinista (Temp 0)
Envía el mismo prompt creativo (ej., "Nombra un color ficticio") 3 veces con `temperature=0.0`. Observa los resultados.

### Parte 2: Creativo (Temp 1)
Envía el mismo prompt 3 veces con `temperature=1.0`. Observa las diferencias.

## 💻 Código de Inicio

```python
def obtener_completado(temp):
    # TODO: Llamar API con temperature=temp
    pass

print("Temp 0.0:")
for _ in range(3):
    print(obtener_completado(0.0))

print("Temp 1.0:")
for _ in range(3):
    print(obtener_completado(1.0))
```

## ✅ Salida Esperada

```
Temp 0 debería ser idéntico. Temp 1 debería variar.
```

## 🧪 Casos de Prueba

Ejecutar script.

## 🎁 Pistas

<details>
<summary>Pista 1: Parámetro</summary>

Pasa `temperature=x` a `client.messages.create`.
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
# Ver lógica del código de inicio
```
</details>

## 🚀 Extensiones

Prueba temperatura 0.5.

## 📖 Resultados de Aprendizaje

- ✅ Control de aleatoriedad
- ✅ Entendimiento de parámetros

## 🔗 Lecciones Relacionadas
- [Parámetros de Solicitud](../../modulos/modulo1_fundamentos/08_solicitud_respuesta.md)

## ❓ Problemas Comunes

Ninguno

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio. Avanza al [Ejercicio 6: Chatbot en Streaming](../intermedio/01_chatbot_streaming.md)
