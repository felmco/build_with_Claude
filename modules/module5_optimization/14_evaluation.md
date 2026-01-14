# 5.4 Building Evaluation Frameworks

Prompt Engineering is engineering. You need tests.

## Components of an Eval
1. **Dataset:** Inputs and "Golden" answers (Ground Truth).
2. **Runner:** Code to send inputs to Claude.
3. **Grader:** Logic to check if Claude's output matches the Golden answer.

## Types of Grading
1. **Exact Match:** Good for extraction (JSON).
2. **Fuzzy Match:** "Contains the keyword X".
3. **LLM-as-a-Judge:** Ask another LLM (e.g., Opus) to rate the answer on a scale of 1-5.

## Next Steps
- [Automated Testing](./15_automated_testing.md).
