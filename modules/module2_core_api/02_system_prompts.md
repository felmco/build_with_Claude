# 2.1 System Prompts

System prompts are the primary way to influence Claude's behavior, persona, and constraints throughout a conversation.

## What is a System Prompt?

A system prompt is text provided to Claude that sits "above" the conversation. It sets the context, role, and rules for how Claude should behave.

### Basic Usage

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful assistant who speaks like a pirate.",
    messages=[
        {"role": "user", "content": "Hello there!"}
    ]
)
print(message.content[0].text)
```

## Best Practices for System Prompts

### 1. Assign a Role
Give Claude a specific persona. This helps frame its knowledge and tone.

```python
system = "You are a senior Python backend developer conducting a code review."
```

### 2. Define Clear Constraints
Tell Claude what it should *not* do.

```python
system = """
You are a customer support agent.
- Be polite and professional.
- Do NOT make up information about our products.
- If you don't know the answer, say "I don't know" and refer them to support@example.com.
"""
```

### 3. Specify Output Format
If you need JSON, Markdown, or a specific structure, define it here.

```python
system = """
You are a data extraction tool.
Always respond with valid JSON in the following format:
{
  "name": "string",
  "age": "integer",
  "occupation": "string"
}
"""
```

### 4. Use XML Tags for Structure
For complex prompts, use XML tags to separate sections.

```python
system = """
<role>
You are an expert academic editor.
</role>

<task>
Review the user's paper for clarity, grammar, and flow.
</task>

<style>
Maintain a formal, academic tone.
</style>
"""
```

## Advanced Techniques

### Role Prompting
Assigning a detailed role can significantly improve performance on complex tasks.

**Example: Legal Analysis**
```python
system = """
You are a veteran intellectual property lawyer with 20 years of experience.
Your task is to analyze the provided contract clauses for potential risks.
Focus specifically on indemnification and liability caps.
"""
```

### Chain of Thought in System Prompts
You can instruct Claude to think before answering within the system prompt to improve reasoning.

```python
system = """
You are a math tutor. When solving problems, first think through the steps step-by-step
inside <thinking> tags, and then provide the final answer to the student.
"""
```

## Common Pitfalls

- **Putting instructions in the user message:** While it works, the system prompt is more robust for persistent instructions.
- **Being too vague:** "Be helpful" is less effective than "Be concise, technical, and direct."
- **Conflicting instructions:** Ensure your constraints don't contradict your task description.

## Next Steps
- Learn how to manage [Conversations](./03_conversations.md).
