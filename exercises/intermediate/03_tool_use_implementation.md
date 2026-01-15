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
            "op": {"type": "string", "enum": ["add", "sub"]},
            "a": {"type": "number"},
            "b": {"type": "number"}
        }
    }
}]

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
# See Module 3 examples
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
