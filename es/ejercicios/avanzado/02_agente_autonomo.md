# Ejercicio 2: Agente Autónomo

## 🎯 Objetivo
Crear un agente que pueda usar herramientas en un bucle para resolver una tarea de varios pasos (ej., investigar un tema y escribir un resumen).

## ⏱️ Tiempo
60 minutos

## 📚 Requisitos Previos
- Uso de Herramientas (Intermedio)
- Bucles y gestión de estado

## 🎓 Nivel de Dificultad
⭐⭐⭐ Avanzado

## 📝 Instrucciones

### Parte 1: Definir Herramientas
Define al menos 2 herramientas:
- `buscar_web(query)`: Simula una búsqueda (devuelve cadenas predefinidas).
- `escribir_archivo(nombre, contenido)`: Guarda el resultado.

### Parte 2: El Bucle del Agente
Implementa un bucle `while`:
1. Enviar historial a Claude.
2. ¿Claude quiere usar una herramienta?
3. Si SÍ -> Ejecutar herramienta -> Añadir resultado al historial -> Repetir.
4. Si NO -> Imprimir respuesta final -> Romper bucle.

## 💻 Código de Inicio

```python
import os
from anthropic import Anthropic

client = Anthropic()

tools = [
    {
        "name": "buscar",
        "description": "Buscar información",
        "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}}
    },
    {
        "name": "finalizar",
        "description": "Entregar respuesta final",
        "input_schema": {"type": "object", "properties": {"respuesta": {"type": "string"}}}
    }
]

def buscar(q):
    return "Python fue creado por Guido van Rossum en 1991."

def run_agent(objetivo):
    messages = [{"role": "user", "content": objetivo}]
    
    while True:
        # TODO: Llamar a Claude con herramientas
        # TODO: Manejar uso de herramientas
        pass
```

## ✅ Salida Esperada

El agente debe llamar a `buscar`, obtener el resultado, y luego llamar a `finalizar` con la respuesta correcta.

## 🎁 Pistas

<details>
<summary>Pista 1: Estructura Assistant -> User</summary>

Cuando envías el resultado de una herramienta, debe ser un mensaje con `role: user` y contenido tipo `tool_result`.
</details>

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

Ver el proyecto `3_agente_revision_codigo` para una implementación completa de bucle de agente.
</details>

## 📖 Resultados de Aprendizaje

- ✅ Ciclos de razonamiento-acción (ReAct)
- ✅ Encadenamiento de herramientas
- ✅ Gestión de estado compleja
