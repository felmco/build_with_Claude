# Ejercicio 4: Q&A Basado en Contexto

## 🎯 Objetivo
Construye un sistema que responda preguntas basadas SOLO en un contexto de texto proporcionado.

## ⏱️ Tiempo
25 minutos

## 📚 Requisitos Previos
- Formateo de cadenas

## 🎓 Nivel de Dificultad
⭐ Principiante

## 📝 Instrucciones

### Parte 1: El Contexto
Define una variable de cadena que contenga información específica (ej., un mini documento de política).

### Parte 2: El Prompt
Construye un prompt que inyecte este contexto e instruya a Claude a responder preguntas del usuario usando solo ese contexto.

## 💻 Código de Inicio

```python
contexto = """
La política de devoluciones permite devoluciones dentro de los 30 días. 
Se requiere recibo. Los reembolsos tardan 5-7 días hábiles.
"""

pregunta = "¿Puedo devolver sin recibo?"

# TODO: Construir prompt con contexto y pregunta
```

## ✅ Salida Esperada

```
No, se requiere un recibo para las devoluciones.
```

## 🧪 Casos de Prueba

Preguntar sobre algo que no está en el texto -> Debería decir 'No lo sé'.

## 🎁 Pistas

<details>
<summary>Pista 1: Etiquetas XML</summary>

Usa etiquetas <context> para delimitar el texto.
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
prompt = f"""
Responde a la pregunta basándote solo en el siguiente contexto:

<context>
{contexto}
</context>

Pregunta: {pregunta}
"""

```
</details>

## 🚀 Extensiones

Cargar contexto desde un archivo.

## 📖 Resultados de Aprendizaje

- ✅ Inyección de contexto
- ✅ Fundamentación de respuestas

## 🔗 Lecciones Relacionadas
- [Ingeniería de Prompts](../../modulos/modulo5_optimizacion/01_ingenieria_prompts.md)

## ❓ Problemas Comunes

¿El modelo usa conocimiento externo? Añade 'Responde solo usando el texto proporcionado'.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio. Avanza al [Ejercicio 5: Experimentos de Temperatura](05_experimentos_temperatura.md)
