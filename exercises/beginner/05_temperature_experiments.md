# Exercise 5: Temperature Experiments

## 🎯 Objective
Observe how the 'temperature' parameter affects output randomness.

## ⏱️ Time
15 minutes

## 📚 Prerequisites
None

## 🎓 Difficulty Level
⭐ Beginner

> ⚠️ **Model note:** Claude Fable 5.1, Opus 5.5 and Sonnet 5.5 reject non-default `temperature`. Run this exercise with `model="claude-haiku-4-5"`. As a bonus, repeat it on `claude-sonnet-5-5` and see the 400 error for yourself, then compare how different `effort` levels change the answer.

## 📝 Instructions

### Part 1: Deterministic (Temp 0)
Send the same creative prompt (e.g., "Name a fictional color") 3 times with `temperature=0.0`. Observe results.

### Part 2: Creative (Temp 1)
Send the same prompt 3 times with `temperature=1.0`. Observe differences.

## 💻 Starter Code

```python
import anthropic

client = anthropic.Anthropic()

def get_completion(temp):
    # TODO: Call API with temperature=temp (use model="claude-haiku-4-5")
    pass

print("Temp 0.0:")
for _ in range(3):
    print(get_completion(0.0))

print("Temp 1.0:")
for _ in range(3):
    print(get_completion(1.0))
```

## ✅ Expected Output

```
Temp 0.0 should give identical or near-identical answers (low temperature is not a hard determinism guarantee). Temp 1.0 should vary more.
```

## 🧪 Test Cases

Run script.

## 🎁 Hints

<details>
<summary>Hint 1: Parameter</summary>

Pass `temperature=x` to `client.messages.create`.
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
import anthropic

client = anthropic.Anthropic()

def get_completion(temp, model="claude-haiku-4-5"):
    response = client.messages.create(
        model=model,
        max_tokens=50,
        temperature=temp,
        messages=[{"role": "user", "content": "Name a fictional color. Reply with just the name."}],
    )
    return response.content[0].text

print("Temp 0.0:")
for _ in range(3):
    print(" ", get_completion(0.0))

print("Temp 1.0:")
for _ in range(3):
    print(" ", get_completion(1.0))

# Bonus: Sonnet 5.5 rejects a non-default temperature with a 400 error
try:
    get_completion(0.0, model="claude-sonnet-5-5")
except anthropic.BadRequestError as e:
    print("As expected:", e)
```
</details>

## 🚀 Extensions

Try temperature 0.5.

## 📖 Learning Outcomes

- ✅ Controlling randomness
- ✅ Understanding parameters

## 🔗 Related Lessons
- [Request Parameters](../../modules/module1_foundation/08_request_response.md)

## ❓ Common Issues

None

## 🎉 Completion

Congratulations! You've completed the exercise.
