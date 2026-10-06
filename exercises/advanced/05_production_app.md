# Exercise 05: Production Readiness

## 🎯 Objective
Advanced implementation of Production Readiness

## ⏱️ Time
60+ minutes

## 📚 Prerequisites
- Module 4/5

## 🎓 Difficulty Level
⭐⭐⭐ Advanced

## 📝 Instructions

Refer to Module 4/5 materials to implement this advanced system.

## 💻 Starter Code

```python
import anthropic

client = anthropic.Anthropic(max_retries=3, timeout=60.0)

# TODO: wrap calls with logging, usage/cost tracking and error handling
# (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APIStatusError)
```

## ✅ Expected Output

```
Working system
```

## 🧪 Test Cases

Production tests

## 🎁 Hints

Cover: retries and timeouts (the SDK retries 429/5xx automatically; tune `max_retries` and `timeout`), logging of `usage` and request ids, prompt caching, token counting with `client.messages.count_tokens`, and tests/evals.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
# Reference outline: see Module 5 (error handling, observability, deployment) and the
# projects folder for a complete application skeleton.
```
</details>

## 🚀 Extensions

Scale it up.

## 📖 Learning Outcomes

- ✅ Advanced Architecture

## 🔗 Related Lessons
- Module 4/5

## ❓ Common Issues

Complexity management

## 🎉 Completion

Congratulations! You've completed the exercise.
