# Exercise 5: Temperature Experiments

## 🎯 Objective
Observe how the 'temperature' parameter affects output randomness.

## ⏱️ Time
15 minutes

## 📚 Prerequisites
None

## 🎓 Difficulty Level
⭐ Beginner

## 📝 Instructions

### Part 1: Deterministic (Temp 0)
Send the same creative prompt (e.g., "Name a fictional color") 3 times with `temperature=0.0`. Observe results.

### Part 2: Creative (Temp 1)
Send the same prompt 3 times with `temperature=1.0`. Observe differences.

## 💻 Starter Code

```python
def get_completion(temp):
    # TODO: Call API with temperature=temp
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
Temp 0 should be identical. Temp 1 should vary.
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
# See starter code logic
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
