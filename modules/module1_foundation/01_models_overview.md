# 1.1 Available Models and Capabilities

## Introduction
Claude offers multiple models, each optimized for different use cases. Understanding these models will help you choose the right one for your application.

## Current Claude Models (2026)

### Claude Opus 4.5
**Model ID**: `claude-opus-4-5-20251101`

**Best For**:
- Complex reasoning tasks
- Advanced code generation
- Detailed analysis and research
- Tasks requiring highest intelligence

**Characteristics**:
- Highest capability level
- Most expensive option
- Slower response times
- Best for quality-critical applications

**Use Cases**:
```
✅ Complex software architecture design
✅ Advanced mathematical problem solving
✅ Detailed legal or technical document analysis
✅ Multi-step reasoning tasks
✅ Research and strategic planning
```

### Claude Sonnet 4.5
**Model ID**: `claude-sonnet-4-5-20250929`

**Best For**:
- Most production applications
- Balanced performance and speed
- General-purpose tasks
- Cost-effective solutions

**Characteristics**:
- Excellent balance of capability and speed
- Most popular choice for production
- Moderate pricing
- Fast response times

**Use Cases**:
```
✅ Chatbots and conversational AI
✅ Content generation and editing
✅ Code assistance and review
✅ Data analysis and summarization
✅ Customer support automation
```

### Claude Haiku 3.5
**Model ID**: `claude-3-5-haiku-20241022`

**Best For**:
- High-volume applications
- Real-time responses
- Simple tasks
- Budget-conscious projects

**Characteristics**:
- Fastest response times
- Most cost-effective
- Lower capability than Sonnet/Opus
- Great for straightforward tasks

**Use Cases**:
```
✅ Simple classification tasks
✅ Quick Q&A systems
✅ Batch processing large datasets
✅ Real-time chat applications
✅ Simple content moderation
```

## Model Comparison Table

| Feature | Haiku 3.5 | Sonnet 4.5 | Opus 4.5 |
|---------|-----------|------------|----------|
| Speed | ⚡⚡⚡ Fastest | ⚡⚡ Fast | ⚡ Moderate |
| Intelligence | 🧠 Good | 🧠🧠 Excellent | 🧠🧠🧠 Best |
| Cost | 💰 Lowest | 💰💰 Moderate | 💰💰💰 Highest |
| Context Window | 200K tokens | 200K tokens | 200K tokens |
| Best Use | High volume | Production | Complex tasks |

## Token Limits

All Claude models support:
- **Context Window**: 200,000 tokens (~150,000 words)
- **Output Tokens**: Up to 8,192 tokens per request (configurable)

## Model Capabilities

### All Models Support:
- ✅ Text generation and conversation
- ✅ Code understanding and generation
- ✅ Multi-language support (English, Spanish, French, German, etc.)
- ✅ JSON mode for structured outputs
- ✅ Function/tool calling
- ✅ Vision (image understanding)
- ✅ Long context processing

### Advanced Features (Model-Specific):
- **Extended Thinking**: Available on select models for complex reasoning
- **Computer Use**: Beta feature for desktop automation

## Choosing Your Model: Quick Decision Tree

```
Start Here
    |
    ├─ Need highest quality reasoning? → Use Opus 4.5
    |
    ├─ Need fastest responses? → Use Haiku 3.5
    |
    ├─ Need best balance? → Use Sonnet 4.5 ⭐ (Recommended for most)
    |
    └─ Not sure? → Start with Sonnet 4.5, optimize later
```

## Python Example: Checking Model Capabilities

```python
from anthropic import Anthropic

client = Anthropic()

# Dictionary of available models
MODELS = {
    "haiku": "claude-3-5-haiku-20241022",
    "sonnet": "claude-sonnet-4-5-20250929",
    "opus": "claude-opus-4-5-20251101"
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

1. **Start with Sonnet 4.5**: It offers the best balance for most applications
2. **Prototype First**: Test with Sonnet before optimizing costs
3. **Use Haiku for Scale**: Once your application works, consider Haiku for high-volume tasks
4. **Reserve Opus for Complexity**: Use Opus only when Sonnet doesn't meet your quality needs
5. **Monitor Performance**: Track quality, speed, and cost metrics to optimize

## Model Versions and Updates

Claude models are versioned with release dates:
- Example: `claude-sonnet-4-5-20250929` (released September 29, 2025)
- Always use the latest stable version for production
- Older versions may be deprecated over time
- Check release notes for breaking changes

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
        return "claude-3-5-haiku-20241022"
    elif speed_priority and task_complexity != "complex":
        return "claude-3-5-haiku-20241022"
    elif task_complexity == "complex":
        return "claude-opus-4-5-20251101"
    else:
        return "claude-sonnet-4-5-20250929"  # Default choice
```

## Next Steps
- Proceed to [Choosing the Right Model](./02_model_selection.md)
- Learn about [Model Pricing and Limits](./03_pricing_limits.md)

## Additional Resources
- [Official Model Comparison](https://platform.claude.com/docs/en/models/overview)
- [Anthropic Pricing Page](https://www.anthropic.com/pricing)
- [Model Release Notes](https://platform.claude.com/docs/en/release-notes)
