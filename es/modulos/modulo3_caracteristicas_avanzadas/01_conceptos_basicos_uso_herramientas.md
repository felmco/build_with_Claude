# 3.1 Introducción al Uso de Herramientas

## Introducción
El uso de herramientas (también llamado llamada a funciones o function calling) permite a Claude interactuar con herramientas externas, APIs y funciones. Claude puede decidir cuándo usar herramientas, qué herramientas usar y qué parámetros proporcionar.

## ¿Por Qué Usar Herramientas?

### Sin Uso de Herramientas
Claude no tiene acceso a:
- Datos en tiempo real (clima, precios de acciones, noticias)
- Tus bases de datos o sistemas
- APIs externas
- Cálculos personalizados
- Sistemas de archivos

### Con Uso de Herramientas
Claude puede:
- ✅ Obtener información en tiempo real
- ✅ Consultar bases de datos
- ✅ Llamar a APIs externas
- ✅ Realizar cálculos
- ✅ Ejecutar código
- ✅ Acceder a tus sistemas

## Cómo Funciona el Uso de Herramientas

### El Flujo
```
1. El usuario hace una pregunta
2. Claude decide que necesita una herramienta
3. Claude devuelve una petición de uso de herramienta
4. Tu código ejecuta la herramienta
5. Envías el resultado de la herramienta de vuelta a Claude
6. Claude usa el resultado para responder la pregunta
```

### Flujo de Ejemplo
```
Usuario: "¿Qué tiempo hace en París?"
  ↓
Claude: "Necesito usar weather_tool con location='Paris'"
  ↓
Tu código: Llama a la API del clima → "Soleado, 22°C"
  ↓
Claude: "El tiempo en París es soleado con una temperatura de 22°C"
```

## Ejemplo Básico de Uso de Herramientas

### Paso 1: Definir Tu Herramienta

```python
from anthropic import Anthropic

client = Anthropic()

# Definir una herramienta de calculadora simple
tools = [
    {
        "name": "calculator",
        "description": "Performs basic arithmetic operations. Use this when you need to calculate numbers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "The first number"
                },
                "b": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    }
]
```

### Paso 2: Hacer la Petición Inicial

```python
user_message = "What is 125 multiplied by 8?"

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": user_message}
    ]
)

print("Response:", message)
```

### Paso 3: Manejar el Uso de Herramienta

```python
# Comprobar si Claude quiere usar una herramienta
if message.stop_reason == "tool_use":
    # Encontrar el bloque de uso de herramienta
    tool_use_block = next(
        block for block in message.content
        if block.type == "tool_use"
    )

    tool_name = tool_use_block.name
    tool_input = tool_use_block.input

    print(f"Claude quiere usar: {tool_name}")
    print(f"Con entradas: {tool_input}")
    # Salida:
    # Claude quiere usar: calculator
    # Con entradas: {'operation': 'multiply', 'a': 125, 'b': 8}
```

### Paso 4: Ejecutar la Herramienta

```python
def calculator(operation: str, a: float, b: float) -> float:
    """Ejecutar operaciones de calculadora"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Ejecutar la herramienta
result = calculator(**tool_input)
print(f"Tool result: {result}")  # 1000
```

### Paso 5: Enviar Resultado de Vuelta a Claude

```python
# Construir mensajes con resultado de herramienta
messages = [
    {"role": "user", "content": user_message},
    {"role": "assistant", "content": message.content},
    {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": str(result)
            }
        ]
    }
]

# Obtener respuesta final
final_response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print(final_response.content[0].text)
# Salida: "125 multiplied by 8 equals 1000."
```

## Ejemplo Completo Funcional

**calculator_tool.py**:
```python
#!/usr/bin/env python3
"""Ejemplo completo de uso de herramienta con calculadora"""

from anthropic import Anthropic
from typing import Dict, Any

def calculator(operation: str, a: float, b: float) -> float:
    """Realizar operaciones aritméticas"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    return operations[operation](a, b)

def use_tool(user_message: str) -> str:
    """Enviar mensaje con capacidad de uso de herramientas"""
    client = Anthropic()

    # Definir herramienta
    tools = [
        {
            "name": "calculator",
            "description": "Performs basic arithmetic operations (add, subtract, multiply, divide)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation"
                    },
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    ]

    # Petición inicial
    messages = [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Manejar uso de herramienta
    if response.stop_reason == "tool_use":
        # Extraer uso de herramienta
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Ejecutar herramienta
        print(f"🔧 Ejecutando herramienta: {tool_use_block.name}")
        print(f"📥 Entrada: {tool_use_block.input}")

        result = calculator(**tool_use_block.input)
        print(f"📤 Resultado: {result}\n")

        # Continuar conversación con resultado
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": str(result)
                    }
                ]
            }
        ]

        # Obtener respuesta final
        final_response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        return final_response.content[0].text

    # Si no hay uso de herramienta, devolver respuesta directa
    return response.content[0].text

def main():
    """Probar herramienta calculadora"""
    questions = [
        "What is 1234 plus 5678?",
        "Calculate 99 divided by 11",
        "What is 15 times 23?",
        "What is 1000 minus 742?"
    ]

    for question in questions:
        print(f"❓ Pregunta: {question}")
        answer = use_tool(question)
        print(f"💬 Respuesta: {answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

## Herramienta del Mundo Real: API del Clima

**weather_tool.py**:
```python
#!/usr/bin/env python3
"""Ejemplo de herramienta del clima"""

from anthropic import Anthropic
import requests
from typing import Dict

def get_weather(location: str, unit: str = "celsius") -> Dict:
    """
    Obtener clima para una ubicación (implementación simulada)
    En producción, usa una API real como OpenWeatherMap
    """
    # Datos simulados para demostración
    mock_weather = {
        "paris": {"temp": 22, "condition": "sunny", "humidity": 65},
        "london": {"temp": 15, "condition": "cloudy", "humidity": 75},
        "tokyo": {"temp": 28, "condition": "rainy", "humidity": 85},
        "new york": {"temp": 25, "condition": "partly cloudy", "humidity": 70}
    }

    location_lower = location.lower()
    if location_lower in mock_weather:
        data = mock_weather[location_lower]
        return {
            "location": location,
            "temperature": data["temp"],
            "unit": unit,
            "condition": data["condition"],
            "humidity": data["humidity"]
        }
    else:
        return {"error": f"Weather data not available for {location}"}

def weather_assistant(user_message: str) -> str:
    """Asistente con herramienta de clima"""
    client = Anthropic()

    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a specific location. Returns temperature, conditions, and humidity.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'Paris', 'London', 'Tokyo')"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                        "default": "celsius"
                    }
                },
                "required": ["location"]
            }
        }
    ]

    messages = [{"role": "user", "content": user_message}]

    # Petición inicial
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Manejar uso de herramienta
    if response.stop_reason == "tool_use":
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Ejecutar API del clima
        weather_data = get_weather(**tool_use_block.input)
        print(f"🌤️  Clima obtenido: {weather_data}\n")

        # Continuar conversación
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": str(weather_data)
                    }
                ]
            }
        ]

        final_response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        return final_response.content[0].text

    return response.content[0].text

def main():
    """Probar herramienta del clima"""
    questions = [
        "What's the weather like in Paris?",
        "Is it raining in Tokyo?",
        "What's the temperature in London?"
    ]

    for question in questions:
        print(f"❓ {question}")
        answer = weather_assistant(question)
        print(f"💬 {answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

## Mejores Prácticas de Definición de Herramientas

### Buena Definición de Herramienta
```python
{
    "name": "search_database",
    "description": "Searches the user database for users matching specific criteria. Use this when the user asks about finding or looking up users.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Can include name, email, or user ID."
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 10)",
                "default": 10
            }
        },
        "required": ["query"]
    }
}
```

### ¿Qué la Hace Buena?
✅ **Nombre claro**: Describe lo que hace la herramienta
✅ **Descripción detallada**: Explica cuándo usarla
✅ **Parámetros bien documentados**: Cada parámetro tiene una descripción clara
✅ **Valores predeterminados sensatos**: Proporciona valores por defecto donde esapropiado
✅ **Campos requeridos marcados**: Claude sabe qué es obligatorio

### Mala Definición de Herramienta
```python
{
    "name": "tool1",  # ❌ Nombre poco claro
    "description": "Does stuff",  # ❌ Descripción vaga
    "input_schema": {
        "type": "object",
        "properties": {
            "data": {  # ❌ Nombre de parámetro genérico
                "type": "string"  # ❌ Sin descripción
            }
        },
        "required": ["data"]
    }
}
```

## Patrones Comunes

### Patrón 1: Uso de Herramienta Única
```python
# Usuario hace pregunta → Claude usa herramienta → Claude responde
# Ejemplo: "¿Cuánto es 5 + 3?" → usar calculadora → "La respuesta es 8"
```

### Patrón 2: Múltiples Llamadas a Herramientas
```python
# Usuario hace pregunta compleja requiriendo múltiples herramientas
# Ejemplo: "¿Qué tiempo hace en París y Londres?"
#   → usar herramienta de clima para París
#   → usar herramienta de clima para Londres
#   → combinar resultados en respuesta
```

### Patrón 3: Cadena de Herramientas (Tool Chain)
```python
# Las herramientas llaman a otras herramientas en secuencia
# Ejemplo: "Encuentra al usuario X y obtén su historial de pedidos"
#   → search_user("X")
#   → get_orders(user_id)
#   → responder con información combinada
```

### Patrón 4: Ninguna Herramienta Necesaria
```python
# Claude decide que la herramienta no es necesaria
# Ejemplo: "¿Cuál es la capital de Francia?"
#   → Claude sabe esto, responde directamente sin herramientas
```

## Depurando el Uso de Herramientas

### Registrar Todas las Llamadas a Herramientas
```python
def log_tool_use(tool_name: str, tool_input: dict, result: any):
    """Registrar uso de herramienta para depuración"""
    print(f"""
    🔧 REGISTRO DE USO DE HERRAMIENTA
    ═════════════════════════════════
    Herramienta: {tool_name}
    Entrada: {tool_input}
    Resultado: {result}
    """)

# Usar en tu manejador de herramientas
if response.stop_reason == "tool_use":
    tool_use_block = next(...)
    result = execute_tool(tool_use_block.name, tool_use_block.input)
    log_tool_use(tool_use_block.name, tool_use_block.input, result)
```

### Validar Entradas de Herramientas
```python
def validate_tool_input(tool_name: str, tool_input: dict) -> bool:
    """Validar entradas de herramienta antes de ejecución"""
    if tool_name == "calculator":
        required = ["operation", "a", "b"]
        if not all(key in tool_input for key in required):
            print(f"❌ Campos requeridos faltantes para {tool_name}")
            return False
        if tool_input["operation"] not in ["add", "subtract", "multiply", "divide"]:
            print(f"❌ Operación inválida: {tool_input['operation']}")
            return False
    return True
```

## Manejo de Errores

### Manejar Errores de Herramientas con Elegancia
```python
def safe_tool_execution(tool_name: str, tool_input: dict):
    """Ejecutar herramienta con manejo de errores"""
    try:
        if tool_name == "calculator":
            result = calculator(**tool_input)
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

    except ZeroDivisionError:
        return {"success": False, "error": "Cannot divide by zero"}

    except Exception as e:
        return {"success": False, "error": str(e)}

# Usar en manejador de herramientas
result = safe_tool_execution(tool_use_block.name, tool_use_block.input)

# Enviar resultado de vuelta a Claude
tool_result = {
    "type": "tool_result",
    "tool_use_id": tool_use_block.id,
    "content": str(result) if result["success"] else f"Error: {result['error']}"
}
```

## Referencia Rápida

```python
# 1. Definir herramienta
tools = [{
    "name": "tool_name",
    "description": "What the tool does",
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}]

# 2. Hacer petición con herramientas
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "..."}]
)

# 3. Comprobar uso de herramienta
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
    result = execute_tool(tool_block.name, tool_block.input)

    # 4. Enviar resultado de vuelta
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": str(result)
        }]
    })

    # 5. Obtener respuesta final
    final = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
```

## Próximos Pasos
- Aprende sobre [Construyendo Herramientas Personalizadas](02_herramientas_personalizadas.md)
- Explora [Orquestación Multi-Herramienta](03_multi_herramienta.md)
- Revisa [Mejores Prácticas de Uso de Herramientas](04_mejores_practicas_herramientas.md)

## Recursos Adicionales
- [Documentación Oficial de Uso de Herramientas](https://platform.claude.com/docs/en/agents-and-tools/tool-use)
- [Recetario de Uso de Herramientas](https://github.com/anthropics/anthropic-cookbook)
