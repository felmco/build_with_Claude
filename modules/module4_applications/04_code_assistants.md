# 4.1 Code Assistants

Building a coding assistant requires specific strategies for code generation and understanding.

## System Prompt for Coding

```text
You are an expert software engineer.
- Write clean, efficient, documented code.
- Follow PEP 8 for Python.
- Include error handling.
- Explain your logic briefly before writing code.
```

## Context Awareness
To edit existing code, you must provide the file content.

**Input:**
```xml
<file name="main.py">
def hello():
    print("hi")
</file>

Refactor this function to take a name argument.
```

## Techniques
1. **Fill-in-the-middle (FIM):** Not natively supported by Claude Message API, but you can simulate it by providing "Context Before" and "Context After".
2. **Test Generation:** Ask Claude to write tests *before* the code (TDD).
3. **Docstring Generation:** Send code, ask for docs.

## Tools
- Provide a `read_file` and `write_file` tool to let Claude actually edit your project.

## Next Steps
- Learn about [Agent Architecture](./05_agent_architecture.md).
