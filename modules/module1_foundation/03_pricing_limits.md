# 1.1 Model Pricing and Limits

Understanding the cost structure and rate limits is crucial for building sustainable applications with Claude.

## Pricing Overview (as of 2026)

Pricing is based on **tokens**.
- **Input Tokens**: Text you send to Claude (prompts, documents).
- **Output Tokens**: Text Claude generates.

| Model | Input Cost (per MTok) | Output Cost (per MTok) |
|-------|------------------------|-------------------------|
| **Claude Haiku 3.5** | $0.80 | $4.00 |
| **Claude Haiku 4.5** | $1.00 | $5.00 |
| **Claude Sonnet 4.5** | $3.00 | $15.00 |
| **Claude Opus 4.5** | $5.00 | $25.00 |

*MTok = Million Tokens*

### Prompt Caching Pricing
Prompt caching allows you to cache large contexts (like books, codebases) to reduce input costs.

- **Cache Write**: Higher cost (initial processing)
- **Cache Read**: Significantly lower cost (~10% of standard input)

| Model | Cache Write (5m) | Cache Write (1h) | Cache Read |
|-------|------------------|------------------|------------|
| **Sonnet 4.5** | $3.75 / MTok | $6.00 / MTok | $0.30 / MTok |
| **Haiku 4.5** | $1.25 / MTok | $2.00 / MTok | $0.10 / MTok |

## Rate Limits

Rate limits determine how many requests you can make per minute (RPM) and how many tokens you can consume per minute (TPM). Limits vary by **Tier**.

### Usage Tiers

| Tier | Description | Typical Limits (Sonnet) |
|------|-------------|-------------------------|
| **Free / Tier 1** | New accounts | Low RPM (e.g., 5-50) |
| **Tier 2** | Active usage | Moderate RPM (e.g., 1000) |
| **Tier 3** | High volume | High RPM (e.g., 2000+) |
| **Tier 4** | Enterprise | Custom / Max limits |

*Note: Check your specific limits in the [Anthropic Console](https://console.anthropic.com/settings/limits).*

## Managing Costs

### 1. Estimate Token Counts
Use the tokenizer tool or API to estimate usage.
```python
# Approximate: 1000 tokens ≈ 750 words
word_count = len(text.split())
estimated_tokens = word_count * 1.33
cost = (estimated_tokens / 1_000_000) * 3.00  # For Sonnet Input
```

### 2. Set `max_tokens`
Always set a `max_tokens` limit in your API calls to prevent unexpected large outputs (and costs) if the model loops or generates too much text.

### 3. Use Caching for Long Contexts
If you send the same long document multiple times, use Prompt Caching to save up to 90% on input costs.

## Next Steps
- Set up your environment in [Installing Python and Dependencies](./04_python_setup.md).
