# Ejercicio 3: Uso Básico de Herramientas

## 🎯 Objetivo
Implementa una herramienta calculadora que Claude pueda llamar.

## ⏱️ Tiempo
40 minutos

## 📚 Requisitos Previos
- Módulo 3 Uso de Herramientas

## 🎓 Nivel de Dificultad
⭐⭐ Intermedio

## 📝 Instrucciones

### Parte 1: Definir Herramienta
Define el esquema JSON para una herramienta `calculate` (add, sub, mul, div).

### Parte 2: Analizar Respuesta
Comprueba si Claude quiere usar la herramienta.

### Parte 3: Ejecutar y Devolver
Ejecuta la matemática, devuelve el resultado a Claude.

## 💻 Código de Inicio

```python
tools = [{
    "name": "calculate",
    "description": "Realizar matemáticas",
    "input_schema": {
        "type": "object",
        "properties": {
            "op": {"type": "string", "enum": ["add", "sub", "mul", "div"]},
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["op", "a", "b"]
    }
}]

# TODO: envía "¿Cuánto es 50 + 20?" con tools=tools, comprueba stop_reason,
# ejecuta el cálculo y devuelve un tool_result a Claude.

```
## ✅ Salida Esperada

```
Claude pide usar herramienta, tú imprimes resultado, Claude responde al usuario.
```

## 🧪 Casos de Prueba

¿Cuánto es 50 + 20?

## 🎁 Pistas

<details>
<summary>Pista 1: Razón de Parada</summary>

Comprueba `message.stop_reason == 'tool_use'`
</details>


## ✨ Solución

<details>
<summary>Click para ver solución</summary>

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"

tools = [{
    "name": "calculate",
    "description": "Realiza aritmética básica sobre dos números.",
    "input_schema": {
        "type": "object",
        "properties": {
            "op": {"type": "string", "enum": ["add", "sub", "mul", "div"]},
            "a": {"type": "number"},
            "b": {"type": "number"},
        },
        "required": ["op", "a", "b"],
    },
}]

def run_calculate(op, a, b):
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":
        if b == 0:
            raise ZeroDivisionError("división entre cero")
        return a / b
    raise ValueError(f"operación desconocida {op}")

messages = [{"role": "user", "content": "¿Cuánto es 50 + 20?"}]

while True:
    response = client.messages.create(
        model=MODEL, max_tokens=1024, tools=tools, messages=messages
    )
    if response.stop_reason != "tool_use":
        break

    # Conserva el turno completo del asistente (incluidos los bloques thinking) en el historial
    messages.append({"role": "assistant", "content": response.content})

    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            try:
                result = str(run_calculate(**block.input))
                is_error = False
            except (ValueError, ZeroDivisionError) as e:
                result, is_error = str(e), True
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
                "is_error": is_error,
            })
    messages.append({"role": "user", "content": tool_results})

print("".join(b.text for b in response.content if b.type == "text"))
```</details>

## 🚀 Extensiones

Añade funciones matemáticas más complejas.

## 📖 Resultados de Aprendizaje

- ✅ Llamada a funciones
- ✅ Definiciones de herramientas

## 🔗 Lecciones Relacionadas
- [Conceptos Básicos de Uso de Herramientas](../../modulos/modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md)

## ❓ Problemas Comunes

Esquema JSON inválido.

## 🎉 Finalización

¡Felicidades! Has completado el ejercicio.
