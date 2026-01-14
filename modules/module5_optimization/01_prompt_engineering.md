# 5.1 Prompt Engineering Fundamentals

Prompt engineering is the art of communicating with AI models to get the best possible results.

## The Core Principles

### 1. Be Clear and Direct
- **Bad:** "Write something about cats."
- **Good:** "Write a 300-word blog post about the benefits of adopting senior cats for apartment living."

### 2. Use Examples (Few-Shot)
Providing examples helps the model understand the desired pattern and tone.

### 3. Give Claude a Role
Assigning a persona (e.g., "You are an expert data scientist") helps frame the model's knowledge and style.

### 4. Use XML Tags
XML tags help structure inputs and separate data from instructions.

```xml
<instructions>
Summarize the text below.
</instructions>

<text>
...
</text>
```

## The "Perfect" Prompt Structure

1. **Role:** Who is Claude?
2. **Context:** What is the situation?
3. **Instructions:** What specific steps should it take?
4. **Data:** The input to process.
5. **Output Format:** JSON, Markdown, CSV?
6. **Constraints:** What *not* to do.

## Next Steps
- [Advanced Prompting](./02_advanced_prompting.md).
