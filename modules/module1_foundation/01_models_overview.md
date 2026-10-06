# 1.1 Available Models and Capabilities

## Introduction
Claude offers multiple models, each optimized for different use cases. Understanding these models will help you choose the right one for your application.

## Current Claude Models (October 2026)

> Verified against the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Model lineups change often, so check it (or call the Models API, see below) before you hard-code an ID.

### Claude Fable 5.1
**Model ID**: `claude-fable-5-1`

**Best For**:
- The most demanding reasoning
- Long-horizon, autonomous agentic work
- Cases where your evals on Opus 5.5 at higher effort still fall short

**Characteristics**:
- Most capable widely released model
- Thinking is always on (steer it with `effort`)
- Slowest and most expensive ($10 / $50 per MTok)

### Claude Opus 5.5
**Model ID**: `claude-opus-5-5`

**Best For**:
- Long-running agentic coding and knowledge work
- Complex reasoning and analysis
- A strong default when quality matters most

**Characteristics**:
- Adaptive thinking always on; default effort is `medium`
- 1M-token context, 128K max output
- $4 / $20 per MTok

**Use Cases**:
```
✅ Complex software architecture design
✅ Multi-file refactors and long coding sessions
✅ Detailed legal or technical document analysis
✅ Research and strategic planning
```

### Claude Sonnet 5.5
**Model ID**: `claude-sonnet-5-5`

**Best For**:
- Most production applications
- The best combination of speed and intelligence
- Cost-effective everyday coding, agent, and enterprise work

**Characteristics**:
- Fast, with adaptive thinking (default effort `high`)
- 1M-token context, 128K max output
- $2 / $10 per MTok

**Use Cases**:
```
✅ Chatbots and conversational AI
✅ Content generation and editing
✅ Code assistance and review
✅ Data analysis and summarization
✅ Customer support automation
```

### Claude Haiku 4.5
**Model ID**: `claude-haiku-4-5` (pinned snapshot: `claude-haiku-4-5-20251001`)

**Best For**:
- High-volume applications
- Real-time responses
- Sub-agents and simple tasks
- Budget-conscious projects

**Characteristics**:
- Fastest model with near-frontier intelligence
- 200K-token context, 64K max output
- Uses manual extended thinking (`budget_tokens`), no `effort` parameter
- $1 / $5 per MTok

**Use Cases**:
```
✅ Classification and extraction
✅ Quick Q&A systems
✅ Batch processing large datasets
✅ Real-time chat applications
✅ Content moderation
```

> **Legacy models** (still served): Claude Fable 5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5 and Sonnet 4.6. Older IDs that appear in tutorials online, such as `claude-3-5-haiku-20241022` or `claude-sonnet-4-5-20250929`, are on the deprecation path. See [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

## Model Comparison Table

| Feature | Haiku 4.5 | Sonnet 5.5 | Opus 5.5 | Fable 5.1 |
|---------|-----------|------------|----------|-----------|
| Speed | ⚡⚡⚡ Fastest | ⚡⚡ Fast | ⚡ Moderate | 🐢 Slower |
| Intelligence | 🧠 Near-frontier | 🧠🧠 Excellent | 🧠🧠🧠 Best for most | 🧠🧠🧠🧠 Highest |
| Price (in / out per MTok) | $1 / $5 | $2 / $10 | $4 / $20 | $10 / $50 |
| Context Window | 200K tokens | 1M tokens | 1M tokens | 1M tokens |
| Max Output | 64K tokens | 128K tokens | 128K tokens | 128K tokens |
| Thinking | Extended (`budget_tokens`) | Adaptive | Adaptive (always on) | Adaptive (always on) |
| Best Use | High volume | Production | Agentic coding | Hardest problems |

## Token Limits

Limits differ per model (table above). Do not assume them: query the **Models API** (`client.models.retrieve("claude-sonnet-5-5")`), which returns `max_input_tokens`, `max_tokens` and a `capabilities` object.

## Model Capabilities

### All Models Support:
- ✅ Text generation and conversation
- ✅ Code understanding and generation
- ✅ Multi-language support (English, Spanish, French, German, etc.)
- ✅ Structured outputs (`output_config.format`)
- ✅ Function/tool calling
- ✅ Vision (image understanding)
- ✅ Long context processing

### Advanced Features (Model-Specific):
- **Adaptive Thinking + `effort`**: Claude decides how much to think; you steer depth with `output_config.effort`
- **Computer Use**: Desktop automation through the `computer_toolset_20260801` tool
- **Structured Outputs**: Constrain responses to a JSON schema with `output_config.format`

## Choosing Your Model: Quick Decision Tree

```
Start Here
    |
    ├─ Hardest reasoning / long autonomous runs? → Use Fable 5.1
    |
    ├─ Need highest quality reasoning? → Use Opus 5.5
    |
    ├─ Need fastest responses? → Use Haiku 4.5
    |
    ├─ Need best balance? → Use Sonnet 5.5 ⭐ (Recommended for most)
    |
    └─ Not sure? → Start with Sonnet 5.5, optimize later
```

## Python Example: Checking Model Capabilities

```python
from anthropic import Anthropic

client = Anthropic()

# Dictionary of available models
MODELS = {
    "haiku": "claude-haiku-4-5",
    "sonnet": "claude-sonnet-5-5",
    "opus": "claude-opus-5-5",
    "fable": "claude-fable-5-1",
}

def test_model(model_name: str, prompt: str):
    """Test a specific model with a prompt"""
    response = client.messages.create(
        model=MODELS[model_name],
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

# Example usage
prompt = "Explain quantum computing in one sentence."

print("Testing Haiku:")
print(test_model("haiku", prompt))

print("\nTesting Sonnet:")
print(test_model("sonnet", prompt))

print("\nTesting Opus:")
print(test_model("opus", prompt))
```

## Best Practices

1. **Start with Sonnet 5.5**: It offers the best balance for most applications
2. **Prototype First**: Test with Sonnet before optimizing costs
3. **Use Haiku for Scale**: Once your application works, consider Haiku for high-volume tasks
4. **Reserve Opus and Fable for Complexity**: Move up only when Sonnet doesn't meet your quality needs
5. **Monitor Performance**: Track quality, speed, and cost metrics to optimize

## Model Versions and Updates

Since the 4.6 generation, Claude model IDs are dateless and each one is a **pinned snapshot** (for example `claude-sonnet-5-5`). Do not append date suffixes to them.
- Pick a current model for new work and plan for the retirement dates on the [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) page
- Cloud platforms use their own ID formats: Amazon Bedrock `anthropic.claude-sonnet-5-5`, Google Cloud `claude-sonnet-5-5`
- Re-run your evals when you migrate, because defaults such as `effort` and thinking behaviour change between generations (see the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide))

## Common Misconceptions

❌ **"Opus is always better"**: Not true - Sonnet often performs as well for most tasks
❌ **"Haiku can't handle complex tasks"**: It can, just not as well as Sonnet/Opus
❌ **"You need different code for different models"**: Same API, just change model ID
❌ **"Larger context = better results"**: Not always - focused prompts often work better

## Quick Reference

```python
# Model selection helper
def select_model(task_complexity: str, speed_priority: bool = False, budget_tight: bool = False):
    """Helper function to select appropriate model"""
    if budget_tight and task_complexity == "simple":
        return "claude-haiku-4-5"
    elif speed_priority and task_complexity != "complex":
        return "claude-haiku-4-5"
    elif task_complexity == "complex":
        return "claude-opus-5-5"  # use claude-fable-5-1 for the very hardest problems
    else:
        return "claude-sonnet-5-5"  # Default choice
```

## Next Steps
- Proceed to [Choosing the Right Model](./02_model_selection.md)
- Learn about [Model Pricing and Limits](./03_pricing_limits.md)

## Additional Resources
- [Official Model Comparison](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Release notes](https://platform.claude.com/docs/en/release-notes/overview)
- [Official references hub](../../REFERENCES.md)
