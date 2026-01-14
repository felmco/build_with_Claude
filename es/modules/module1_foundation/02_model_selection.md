# 1.1 Choosing the Right Model

Selecting the optimal Claude model for your application involves balancing three key considerations: **capabilities**, **speed**, and **cost**.

## Decision Matrix

| Feature | Claude Haiku 3.5 | Claude Sonnet 4.5 | Claude Opus 4.5 |
|---------|------------------|-------------------|-----------------|
| **Intelligence** | Good reasoning, fast | High intelligence, balanced | Maximum intelligence |
| **Speed** | ⚡⚡⚡ Very Fast | ⚡⚡ Fast | ⚡ Moderate |
| **Cost** | $ | $$ | $$$ |
| **Context** | 200K | 200K | 200K |

## When to Choose Each Model

### 🚀 Claude Haiku 3.5
**Use when:**
- Speed is critical (real-time chat, autocomplete)
- Volume is high (processing millions of documents)
- Cost is a major constraint
- Tasks are straightforward (classification, extraction, simple Q&A)

**Example Scenarios:**
- Content moderation
- Log analysis
- Simple customer support queries
- Translation of simple text

### ⭐ Claude Sonnet 4.5 (Recommended Starter)
**Use when:**
- You need a balance of high intelligence and speed
- You are building enterprise applications
- You need strong coding or reasoning capabilities
- You are not sure where to start

**Example Scenarios:**
- Coding assistants
- RAG (Retrieval Augmented Generation)
- Data extraction from complex documents
- Marketing copy generation
- Complex customer support

### 🧠 Claude Opus 4.5
**Use when:**
- You need the highest possible quality
- The task involves complex reasoning or creative writing
- Speed and cost are less important than accuracy
- You are handling open-ended research or strategy

**Example Scenarios:**
- Strategic analysis
- Creative writing (novels, screenplays)
- Complex mathematical proofs
- Research synthesis
- High-stakes decision support

## Strategy for Selection

1. **Start with Sonnet**: It handles most use cases well.
2. **Evaluate Performance**: Check if the responses meet your quality standards.
3. **Optimize**:
   - If Sonnet is too slow or expensive, try **Haiku**.
   - If Sonnet lacks nuance or reasoning depth, try **Opus**.

## Model Selection Code Pattern

You can make your code flexible by parameterizing the model choice:

```python
import os
from anthropic import Anthropic

# Define model constants
MODEL_HAIKU = "claude-3-5-haiku-20241022"
MODEL_SONNET = "claude-sonnet-4-5-20250929"
MODEL_OPUS = "claude-opus-4-5-20251101"

client = Anthropic()

def generate_response(prompt, task_type="general"):
    """
    Selects model based on task complexity.
    """
    if task_type == "simple":
        model = MODEL_HAIKU
    elif task_type == "complex":
        model = MODEL_OPUS
    else:
        model = MODEL_SONNET

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

## Next Steps
- Learn about [Model Pricing and Limits](./03_pricing_limits.md) to calculate costs.
