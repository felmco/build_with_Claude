# 4.1 Content Generation Pipelines

Claude excels at generating high-quality content (blogs, emails, reports). A "pipeline" breaks this into steps for better results.

## The Waterfall Pattern

1. **Step 1: Outline**
   - User Topic -> Claude -> Outline.
2. **Step 2: Draft**
   - Outline -> Claude -> First Draft.
3. **Step 3: Critique**
   - Draft -> Claude -> Feedback (Critique).
4. **Step 4: Refine**
   - Draft + Critique -> Claude -> Final Polish.

## Why this works?
LLMs perform better when focusing on one task at a time (reasoning vs. writing vs. editing).

## Example: Marketing Email Generator

```python
# 1. Generate ideas
ideas = client.messages.create(..., prompt="Generate 3 email angles for product X").content[0].text

# 2. Select best (User or Claude)
best_idea = ...

# 3. Write copy
copy = client.messages.create(..., prompt=f"Write email based on: {best_idea}").content[0].text
```

## Next Steps
- [Code Assistants](./04_code_assistants.md).
