# 1.1 Model Pricing and Limits

Understanding the cost structure and rate limits is crucial for building sustainable applications with Claude.

## Pricing Overview (October 2026)

Pricing is based on **tokens**.
- **Input Tokens**: Text you send to Claude (prompts, documents).
- **Output Tokens**: Text Claude generates.

| Model | Input Cost (per MTok) | Output Cost (per MTok) |
|-------|------------------------|-------------------------|
| **Claude Haiku 4.5** | $1.00 | $5.00 |
| **Claude Sonnet 5.5** | $2.00 | $10.00 |
| **Claude Opus 5.5** | $4.00 | $20.00 |
| **Claude Fable 5.1** | $10.00 | $50.00 |

*MTok = Million Tokens. Always confirm on the [official pricing page](https://platform.claude.com/docs/en/about-claude/pricing); prices change.*

- **Batch API**: 50% off input and output for asynchronous work.
- **Thinking tokens** are billed as output tokens.

### Prompt Caching Pricing
Prompt caching allows you to cache large contexts (like books, codebases) to reduce input costs.

- **Cache Write**: 1.25x base input (5-minute) or 2x (1-hour)
- **Cache Read**: a small fraction of the input price (10% on most models; 5% on Opus 5.5; 2.5% on Fable 5.1)

| Model | Cache Write (5m) | Cache Write (1h) | Cache Read |
|-------|------------------|------------------|------------|
| **Haiku 4.5** | $1.25 / MTok | $2.00 / MTok | $0.10 / MTok |
| **Sonnet 5.5** | $2.50 / MTok | $4.00 / MTok | $0.20 / MTok |
| **Opus 5.5** | $5.00 / MTok | $8.00 / MTok | $0.20 / MTok |
| **Fable 5.1** | $12.50 / MTok | $20.00 / MTok | $0.25 / MTok |

## Rate Limits

Rate limits determine how many requests you can make per minute (RPM) and how many tokens you can consume per minute (TPM). Limits vary by **Tier**.

### Usage Tiers

| Tier | Description | Typical Limits (Sonnet) |
|------|-------------|-------------------------|
| **Free / Tier 1** | New accounts | Low RPM (e.g., 5-50) |
| **Tier 2** | Active usage | Moderate RPM (e.g., 1000) |
| **Tier 3** | High volume | High RPM (e.g., 2000+) |
| **Tier 4** | Enterprise | Custom / Max limits |

*Note: Check your specific limits in the [Claude Console](https://platform.claude.com/settings/limits) and the [Rate limits docs](https://platform.claude.com/docs/en/api/rate-limits).*

## Managing Costs

### 1. Estimate Token Counts
Use the token counting API (`client.messages.count_tokens`) to measure usage. Current models share a newer tokenizer that produces more tokens per word than older ones, so re-baseline when you migrate.
```python
# Approximate: 1000 tokens ≈ 750 words
word_count = len(text.split())
estimated_tokens = word_count * 1.33
cost = (estimated_tokens / 1_000_000) * 2.00  # Sonnet 5.5 input price

# Better: count exactly with the API (no tiktoken)
# n = client.messages.count_tokens(model="claude-sonnet-5-5", messages=[...]).input_tokens
```

### 2. Set `max_tokens`
Always set a `max_tokens` limit in your API calls to prevent unexpected large outputs (and costs) if the model loops or generates too much text.

### 3. Use Caching for Long Contexts
If you send the same long document multiple times, use Prompt Caching to save up to 90% or more on input costs.

## Next Steps
- Set up your environment in [Installing Python and Dependencies](./04_python_setup.md).
