# Exercise 04: Custom MCP Server

## 🎯 Objective
Advanced implementation of Custom MCP Server

## ⏱️ Time
60+ minutes

## 📚 Prerequisites
- Module 4/5

## 🎓 Difficulty Level
⭐⭐⭐ Advanced

## 📝 Instructions

Refer to Module 4/5 materials to implement this advanced system.

## 💻 Starter Code

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# TODO: add your own tools

if __name__ == "__main__":
    mcp.run()
```

## ✅ Expected Output

```
Working system
```

## 🧪 Test Cases

Production tests

## 🎁 Hints

Use the official `mcp` Python package: `from mcp.server.fastmcp import FastMCP`, create `mcp = FastMCP("name")`, decorate functions with `@mcp.tool()`, and run with `mcp.run()`. Test it with the MCP Inspector or Claude Desktop. See modelcontextprotocol.io for the current docs.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
# Reference outline: extend the FastMCP server above with tools that wrap a real API
# (for example weather lookups), validate inputs, and return clear error messages.
```
</details>

## 🚀 Extensions

Scale it up.

## 📖 Learning Outcomes

- ✅ Advanced Architecture

## 🔗 Related Lessons
- Module 4/5

## ❓ Common Issues

Complexity management

## 🎉 Completion

Congratulations! You've completed the exercise.
