# 5.4 Automated Testing

Integrate evals into your CI/CD.

## Pattern
1. Developer changes prompt.
2. Push to Git.
3. CI Pipeline runs `pytest`.
4. `pytest` loads 20 sample inputs, calls Claude, runs Graders.
5. If accuracy drops below 95%, Fail Build.

## Tools
- **Pytest:** Standard Python runner.
- **DeepEval:** Open source LLM testing framework.

## Next Steps
- [A/B Testing Prompts](./16_ab_testing.md).
