# 4.5 Testing Claude Applications

## Unit Tests
Test your tools and helper functions.
- "Does `calculator(2, 2)` return 4?"

## Evals (Evaluation)
Test the model's behavior.
- **Dataset:** 50 Q&A pairs.
- **Metric:** "Answer Similarity" or "Factuality".
- **LLM-as-a-Judge:** Ask a stronger model (e.g. `claude-opus-5-5`) to grade a cheaper model's answer (e.g. `claude-haiku-4-5`) against a rubric.

Tests that call the API are slow, cost money and are non-deterministic. Keep unit tests offline by mocking the client, and run evals separately with a fixed dataset and rubric-based grading rather than exact string matches.

## Workflow
1. Change Prompt.
2. Run Evals.
3. If Score increases -> Deploy.

## Congratulations!
You have completed Module 4. You are ready to build sophisticated AI applications.

## Next Module
Proceed to [Module 5: Optimization & Best Practices](../module5_optimization/README.md).
