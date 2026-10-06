# 1.1 Choosing the Right Model

Selecting the optimal Claude model for your application involves balancing three key considerations: **capabilities**, **speed**, and **cost**.

## Decision Matrix

| Feature | Claude Haiku 4.5 | Claude Sonnet 5.5 | Claude Opus 5.5 | Claude Fable 5.1 |
|---------|------------------|-------------------|-----------------|------------------|
| **Intelligence** | Near-frontier, fast | High intelligence, balanced | Very high, agentic coding | Highest |
| **Speed** | ⚡⚡⚡ Very Fast | ⚡⚡ Fast | ⚡ Moderate | 🐢 Slower |
| **Price (in/out per MTok)** | $1 / $5 | $2 / $10 | $4 / $20 | $10 / $50 |
| **Context** | 200K | 1M | 1M | 1M |

## When to Choose Each Model

### 🚀 Claude Haiku 4.5
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

### ⭐ Claude Sonnet 5.5 (Recommended Starter)
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

### 🧠 Claude Opus 5.5
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

### 🔭 Claude Fable 5.1
**Use when:**
- Your evals on Opus 5.5 at higher `effort` still fall short
- The work is long-horizon and autonomous (hours, not minutes)
- The cost of an error is high

Single requests on hard tasks can run for minutes, so stream and plan timeouts accordingly.

## Strategy for Selection

1. **Start with Sonnet**: It handles most use cases well.
2. **Evaluate Performance**: Check if the responses meet your quality standards.
3. **Optimize**:
   - If Sonnet is too slow or expensive, try **Haiku**.
   - If Sonnet lacks nuance or reasoning depth, try **Opus 5.5** (or raise `effort` first).
   - If Opus 5.5 at high effort is still not enough, try **Fable 5.1**.
4. **Tune `effort`** before changing models: `low` for chat and sub-agents, `medium`/`high` for agentic work. Opus 5.5 defaults to `medium`.

## Model Selection Code Pattern

You can make your code flexible by parameterizing the model choice:

```python
import os
from anthropic import Anthropic

# Define model constants
MODEL_HAIKU = "claude-haiku-4-5"
MODEL_SONNET = "claude-sonnet-5-5"
MODEL_OPUS = "claude-opus-5-5"
MODEL_FABLE = "claude-fable-5-1"  # hardest problems

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
- Always confirm IDs and limits in the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
- Learn about [Model Pricing and Limits](./03_pricing_limits.md) to calculate costs.
