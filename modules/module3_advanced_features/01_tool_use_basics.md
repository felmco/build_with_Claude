# 3.1 Tool Use Introduction

## Introduction
Tool use (also called function calling) allows Claude to interact with external tools, APIs, and functions. Claude can decide when to use tools, which tools to use, and what parameters to provide.

## Why Tool Use?

### Without Tool Use
Claude has no access to:
- Real-time data (weather, stock prices, news)
- Your databases or systems
- External APIs
- Custom calculations
- File systems

### With Tool Use
Claude can:
- ✅ Fetch real-time information
- ✅ Query databases
- ✅ Call external APIs
- ✅ Perform calculations
- ✅ Execute code
- ✅ Access your systems

## How Tool Use Works

### The Flow
```
1. User asks a question
2. Claude decides it needs a tool
3. Claude returns tool use request
4. Your code executes the tool
5. You send tool result back to Claude
6. Claude uses result to answer question
```

### Example Flow
```
User: "What's the weather in Paris?"
  ↓
Claude: "I need to use the weather_tool with location='Paris'"
  ↓
Your code: Calls weather API → "Sunny, 22°C"
  ↓
Claude: "The weather in Paris is sunny with a temperature of 22°C"
```

## Basic Tool Use Example

### Step 1: Define Your Tool

```python
from anthropic import Anthropic

client = Anthropic()

# Define a simple calculator tool
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

### Step 2: Make Initial Request

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

### Step 3: Handle Tool Use

```python
# Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
    # Find the tool use block
    tool_use_block = next(
        block for block in message.content
        if block.type == "tool_use"
    )

    tool_name = tool_use_block.name
    tool_input = tool_use_block.input

    print(f"Claude wants to use: {tool_name}")
    print(f"With inputs: {tool_input}")
    # Output:
    # Claude wants to use: calculator
    # With inputs: {'operation': 'multiply', 'a': 125, 'b': 8}
```

### Step 4: Execute the Tool

```python
def calculator(operation: str, a: float, b: float) -> float:
    """Execute calculator operations"""
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

# Execute the tool
result = calculator(**tool_input)
print(f"Tool result: {result}")  # 1000
```

### Step 5: Send Result Back to Claude

```python
# Build messages with tool result
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

# Get final response
final_response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print(final_response.content[0].text)
# Output: "125 multiplied by 8 equals 1000."
```

## Complete Working Example

**calculator_tool.py**:
```python
#!/usr/bin/env python3
"""Complete tool use example with calculator"""

from anthropic import Anthropic
from typing import Dict, Any

def calculator(operation: str, a: float, b: float) -> float:
    """Perform arithmetic operations"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    return operations[operation](a, b)

def use_tool(user_message: str) -> str:
    """Send message with tool use capability"""
    client = Anthropic()

    # Define tool
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

    # Initial request
    messages = [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Handle tool use
    if response.stop_reason == "tool_use":
        # Extract tool use
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute tool
        print(f"🔧 Executing tool: {tool_use_block.name}")
        print(f"📥 Input: {tool_use_block.input}")

        result = calculator(**tool_use_block.input)
        print(f"📤 Result: {result}\n")

        # Continue conversation with result
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

        # Get final response
        final_response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        return final_response.content[0].text

    # If no tool use, return direct response
    return response.content[0].text

def main():
    """Test calculator tool"""
    questions = [
        "What is 1234 plus 5678?",
        "Calculate 99 divided by 11",
        "What is 15 times 23?",
        "What is 1000 minus 742?"
    ]

    for question in questions:
        print(f"❓ Question: {question}")
        answer = use_tool(question)
        print(f"💬 Answer: {answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
```

## Real-World Tool: Weather API

**weather_tool.py**:
```python
#!/usr/bin/env python3
"""Weather tool example"""

from anthropic import Anthropic
import requests
from typing import Dict

def get_weather(location: str, unit: str = "celsius") -> Dict:
    """
    Get weather for a location (mock implementation)
    In production, use a real weather API like OpenWeatherMap
    """
    # Mock data for demonstration
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
    """Assistant with weather tool"""
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

    # Initial request
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    # Handle tool use
    if response.stop_reason == "tool_use":
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute weather API
        weather_data = get_weather(**tool_use_block.input)
        print(f"🌤️  Fetched weather: {weather_data}\n")

        # Continue conversation
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
    """Test weather tool"""
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

## Tool Definition Best Practices

### Good Tool Definition
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

### What Makes It Good?
✅ **Clear name**: Describes what the tool does
✅ **Detailed description**: Explains when to use it
✅ **Well-documented parameters**: Each parameter has clear description
✅ **Sensible defaults**: Provides defaults where appropriate
✅ **Required fields marked**: Claude knows what's mandatory

### Poor Tool Definition
```python
{
    "name": "tool1",  # ❌ Unclear name
    "description": "Does stuff",  # ❌ Vague description
    "input_schema": {
        "type": "object",
        "properties": {
            "data": {  # ❌ Generic parameter name
                "type": "string"  # ❌ No description
            }
        },
        "required": ["data"]
    }
}
```

## Common Patterns

### Pattern 1: Single Tool Use
```python
# User asks question → Claude uses tool → Claude responds
# Example: "What's 5 + 3?" → use calculator → "The answer is 8"
```

### Pattern 2: Multiple Tool Calls
```python
# User asks complex question requiring multiple tools
# Example: "What's the weather in Paris and London?"
#   → use weather tool for Paris
#   → use weather tool for London
#   → combine results in response
```

### Pattern 3: Tool Chain
```python
# Tools call other tools in sequence
# Example: "Find user X and get their order history"
#   → search_user("X")
#   → get_orders(user_id)
#   → respond with combined info
```

### Pattern 4: No Tool Needed
```python
# Claude decides tool isn't needed
# Example: "What is the capital of France?"
#   → Claude knows this, responds directly without tools
```

## Debugging Tool Use

### Log All Tool Calls
```python
def log_tool_use(tool_name: str, tool_input: dict, result: any):
    """Log tool usage for debugging"""
    print(f"""
    🔧 TOOL USE LOG
    ═══════════════
    Tool: {tool_name}
    Input: {tool_input}
    Result: {result}
    """)

# Use in your tool handler
if response.stop_reason == "tool_use":
    tool_use_block = next(...)
    result = execute_tool(tool_use_block.name, tool_use_block.input)
    log_tool_use(tool_use_block.name, tool_use_block.input, result)
```

### Validate Tool Inputs
```python
def validate_tool_input(tool_name: str, tool_input: dict) -> bool:
    """Validate tool inputs before execution"""
    if tool_name == "calculator":
        required = ["operation", "a", "b"]
        if not all(key in tool_input for key in required):
            print(f"❌ Missing required fields for {tool_name}")
            return False
        if tool_input["operation"] not in ["add", "subtract", "multiply", "divide"]:
            print(f"❌ Invalid operation: {tool_input['operation']}")
            return False
    return True
```

## Error Handling

### Handle Tool Errors Gracefully
```python
def safe_tool_execution(tool_name: str, tool_input: dict):
    """Execute tool with error handling"""
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

# Use in tool handler
result = safe_tool_execution(tool_use_block.name, tool_use_block.input)

# Send result back to Claude
tool_result = {
    "type": "tool_result",
    "tool_use_id": tool_use_block.id,
    "content": str(result) if result["success"] else f"Error: {result['error']}"
}
```

## Quick Reference

```python
# 1. Define tool
tools = [{
    "name": "tool_name",
    "description": "What the tool does",
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}]

# 2. Make request with tools
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "..."}]
)

# 3. Check for tool use
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")
    result = execute_tool(tool_block.name, tool_block.input)

    # 4. Send result back
    messages.append({"role": "assistant", "content": response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": str(result)
        }]
    })

    # 5. Get final response
    final = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
```

## Next Steps
- Learn about [Building Custom Tools](./02_custom_tools.md)
- Explore [Multi-Tool Orchestration](./03_multi_tool.md)
- Review [Tool Use Best Practices](./04_tool_best_practices.md)

## Additional Resources
- [Official Tool Use Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use)
- [Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook)
