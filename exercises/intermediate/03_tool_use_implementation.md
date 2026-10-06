# Exercise 3: Basic Tool Use

## 🎯 Objective
Implement a calculator tool that Claude can call.

## ⏱️ Time
40 minutes

## 📚 Prerequisites
- Module 3 Tool Use

## 🎓 Difficulty Level
⭐⭐ Intermediate

## 📝 Instructions

### Part 1: Define Tool
Define the JSON schema for a `calculate` tool (add, sub, mul, div).

### Part 2: Parse Response
Check if Claude wants to use the tool.

### Part 3: Execute and Return
Run the math, give result back to Claude.

## 💻 Starter Code

```python
tools = [{
    "name": "calculate",
    "description": "Perform math",
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

# TODO: send "What is 50 + 20?" with tools=tools, check stop_reason,
# run the calculation, and send a tool_result back to Claude.

```

## ✅ Expected Output

```
Claude asks to use tool, you print result, Claude answers user.
```

## 🧪 Test Cases

What is 50 + 20?

## 🎁 Hints

<details>
<summary>Hint 1: Stop Reason</summary>

Check `message.stop_reason == 'tool_use'`
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-5-5"

tools = [{
    "name": "calculate",
    "description": "Perform basic arithmetic on two numbers.",
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
            raise ZeroDivisionError("division by zero")
        return a / b
    raise ValueError(f"unknown op {op}")

messages = [{"role": "user", "content": "What is 50 + 20?"}]

while True:
    response = client.messages.create(
        model=MODEL, max_tokens=1024, tools=tools, messages=messages
    )
    if response.stop_reason != "tool_use":
        break

    # Keep the full assistant turn (including any thinking blocks) in the history
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
```
</details>

## 🚀 Extensions

Add more complex math functions.

## 📖 Learning Outcomes

- ✅ Function calling
- ✅ Tool definitions

## 🔗 Related Lessons
- [Tool Use Basics](../../modules/module3_advanced_features/01_tool_use_basics.md)

## ❓ Common Issues

Invalid JSON Schema.

## 🎉 Completion

Congratulations! You've completed the exercise.
