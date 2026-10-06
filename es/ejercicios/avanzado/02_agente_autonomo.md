# Ejercicio 2: Agente Autónomo

## 🎯 Objetivo
Crear un agente que pueda usar herramientas en un bucle para resolver una tarea de varios pasos (ej., investigar un tema y escribir un resumen).

## ⏱️ Tiempo
60+ minutos

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
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "buscar",
        "description": "Buscar información",
        "input_schema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"]
        }
    },
    {
        "name": "finalizar",
        "description": "Entregar respuesta final",
        "input_schema": {
            "type": "object",
            "properties": {"respuesta": {"type": "string"}},
            "required": ["respuesta"]
        }
    }
]

def buscar(q):
    return "Python fue creado por Guido van Rossum en 1991."

def run_agent(objetivo):
    messages = [{"role": "user", "content": objetivo}]
    
    while True:
        # TODO: Llamar a Claude con herramientas (model="claude-sonnet-5-5", tools=tools, ...)
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

<details>
<summary>Pista 2: Herramienta de búsqueda web real</summary>

En lugar de simular la búsqueda puedes usar una herramienta del lado del servidor como `{"type": "web_search_20260209", "name": "web_search"}` y repetir el bucle hasta que `stop_reason` sea `end_turn`. Si `stop_reason` es `pause_turn`, devuelve el contenido de la respuesta como turno del asistente para continuar. Limita el número de iteraciones.
</details>

## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"

tools = [
    {
        "name": "buscar",
        "description": "Buscar información",
        "input_schema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    },
    {
        "name": "finalizar",
        "description": "Entregar respuesta final",
        "input_schema": {
            "type": "object",
            "properties": {"respuesta": {"type": "string"}},
            "required": ["respuesta"],
        },
    },
]

def buscar(q):
    return "Python fue creado por Guido van Rossum en 1991."

def run_agent(objetivo, max_turns=5):
    messages = [{"role": "user", "content": objetivo}]

    for _ in range(max_turns):
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=tools, messages=messages
        )
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        # Conserva el turno completo del asistente en el historial
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name == "finalizar":
                return block.input["respuesta"]
            result = buscar(**block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
        messages.append({"role": "user", "content": tool_results})

    return "Se alcanzó el máximo de turnos sin una respuesta final."

if __name__ == "__main__":
    print(run_agent("¿Quién creó Python y cuándo? Usa buscar y luego finalizar."))
```
</details>

## 📖 Resultados de Aprendizaje

- ✅ Ciclos de razonamiento-acción (ReAct)
- ✅ Encadenamiento de herramientas
- ✅ Gestión de estado compleja
