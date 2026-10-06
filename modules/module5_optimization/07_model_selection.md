# 5.2 Model Selection Strategy

Choosing the right model is the biggest optimization lever.

## The Haiku First Strategy
Try to solve the problem with **Claude Haiku 4.5** (`claude-haiku-4-5`) first.
- It is the fastest and cheapest model ($1 / $5 per MTok), with a 200K-token context window (the other current models have 1M).
- Use advanced prompting (Few-Shot, CoT) to boost its capabilities.
- It is a good fit for sub-agents and high-volume routes.

## The Sonnet Default
Use **Claude Sonnet 5.5** (`claude-sonnet-5-5`) for production tasks requiring reliability and nuance ($2 / $10 per MTok, 1M context).

## The Opus Specialist
Use **Claude Opus 5.5** (`claude-opus-5-5`) for:
- Long-running agentic coding and knowledge work.
- Data generation (creating training data for Haiku).
- Complex reasoning that Sonnet fails at.

## The Fable Frontier
Use **Claude Fable 5.1** (`claude-fable-5-1`) only for the hardest, long-horizon work, or when Opus 5.5 at higher effort still fails your evals.

## Tune `effort` before changing models
`output_config.effort` (`low` to `max`) trades thoroughness against token spend within one model. Measure on real requests, tune per route, and judge **cost per completed task**, not cost per request. One model also means one prompt-cache namespace.

## Next Steps
- [Caching Strategies](./08_caching_strategies.md).
- [Cost and intelligence guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence).
