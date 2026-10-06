# 5.1 Advanced Prompting Techniques

Once you master the basics, these techniques allow for complex problem solving.

## 1. Chain of Thought (CoT)
Ask Claude to "Think step-by-step" before answering. This improves reasoning on multi-step problems.

> On current models you can also let the model reason natively: set `thinking={"type": "adaptive"}` and tune `output_config={"effort": ...}` instead of (or in addition to) prompting for steps. See [Chain of Thought](./04_chain_of_thought.md).

```
Question: If I have 3 apples and eat one, then buy two more, how many do I have?
Answer: Let's think step by step.
1. Start with 3 apples.
2. Eat one: 3 - 1 = 2.
3. Buy two: 2 + 2 = 4.
Final Answer: 4.
```

## 2. Prompt Chaining
Breaking a complex task into multiple API calls.
- **Call 1:** Extract data.
- **Call 2:** Analyze data.
- **Call 3:** Format report.

## 3. Metaprompting
Asking Claude to write a prompt for you.
"I want a prompt that classifies customer emails. Write a high-quality prompt for this task."

## Next Steps
- [Few-Shot Learning](./03_few_shot.md).
