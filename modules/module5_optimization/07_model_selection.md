# 5.2 Model Selection Strategy

Choosing the right model is the biggest optimization lever.

## The Haiku First Strategy
Always try to solve the problem with **Claude 3.5 Haiku** first.
- It is significantly faster and cheaper.
- Use advanced prompting (Few-Shot, CoT) to boost its capabilities.

## The Sonnet Default
Use **Claude 3.5 Sonnet** for production tasks requiring reliability and nuance.

## The Opus Specialist
Use **Claude 3 Opus** (or 4.5 Opus) for:
- Data generation (creating training data for Haiku).
- Complex reasoning that Sonnet fails at.

## Next Steps
- [Caching Strategies](./08_caching_strategies.md).
