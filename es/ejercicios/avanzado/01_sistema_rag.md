# Ejercicio 1: Sistema RAG Simple

## 🎯 Objetivo
Construir un sistema de Generación Aumentada por Recuperación (RAG) que permita a Claude responder preguntas basándose en una "base de conocimiento" de documentos de texto.

## ⏱️ Tiempo
45 minutos

## 📚 Requisitos Previos
- Completar ejercicios intermedios
- Conceptos básicos de búsqueda vectorial (similada con coincidencia de cadenas para este ejercicio)

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Base de Conocimiento
Crea una lista de cadenas que actúe como tu "base de datos". Por ejemplo, datos sobre una empresa ficticia.

### Parte 2: Función de Recuperación
Escribe una función `retrieve(query)` simple que busque en tu base de datos y devuelva los 2 trozos de texto más relevantes. (Puedes usar coincidencia de palabras clave simple por ahora).

### Parte 3: El Prompt RAG
Construye un prompt que incluya el contexto recuperado y la pregunta del usuario.

### Parte 4: El Bucle
Haz que sea interactivo: Usuario pregunta -> Recuperar -> Generar -> Respuesta.

## 💻 Código de Inicio

```python
import os
from anthropic import Anthropic

client = Anthropic()

# Tu "Base de Datos Vectorial" falsa
knowledge_base = [
    "La empresa CloudTech fue fundada en 2020.",
    "El CEO de CloudTech es Sarah Connor.",
    "El producto principal es SkyNet, una herramienta de gestión de nubes.",
    "La oficina central está en San Francisco.",
    "El soporte está disponible 24/7 en support@cloudtech.com."
]

def retrieve(query):
    # TODO: Implementar lógica de búsqueda simple
    # Devolver las 2 cadenas más relevantes
    return []

def chat_with_rag(query):
    # TODO: Obtener contexto
    # TODO: Construir prompt con contexto
    # TODO: Enviar a Claude
    pass

if __name__ == "__main__":
    print(chat_with_rag("¿Quién es el CEO?"))
```

## ✅ Salida Esperada

```
El CEO de CloudTech es Sarah Connor.
```

## 🧪 Casos de Prueba

1. **Prueba 1**: Hecho directo
   - Pregunta: "¿Quién es el CEO?"
   - Contexto recuperado: Debe incluir "El CEO de CloudTech es Sarah Connor."
   - Respuesta: Correcta.

2. **Prueba 2**: Hecho irrelevante
   - Pregunta: "¿Cuál es el precio de las acciones?"
   - Contexto recuperado: Probablemente nada relevante.
   - Respuesta: "No tengo esa información."

## 🎁 Pistas

<details>
<summary>Pista 1: Búsqueda Simple</summary>

Usa `if word in document` para encontrar coincidencias.
</details>

<details>
<summary>Pista 2: Inyección de Contexto</summary>

```python
prompt = f"Contexto:\n{context_str}\n\nPregunta: {query}"
```
</details>

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
def retrieve(query):
    # Búsqueda de palabras clave muy simple
    results = []
    for doc in knowledge_base:
        if any(word.lower() in doc.lower() for word in query.split()):
            results.append(doc)
    return results[:2]  # Devolver top 2

def chat_with_rag(query):
    context = retrieve(query)
    context_str = "\n".join(context)
    
    prompt = f"""Responde basándote solo en este contexto:
    <context>
    {context_str}
    </context>
    
    Pregunta: {query}"""
    
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text
```
</details>

## 🚀 Extensiones

1. Usa una biblioteca real como `chromadb` o `faiss` para búsqueda semántica.
2. Carga documentos desde archivos de texto reales.

## 📖 Resultados de Aprendizaje

- ✅ Conceptos fundamentales de RAG
- ✅ Inyección de contexto dinámica
- ✅ Limitaciones de la ventana de contexto
