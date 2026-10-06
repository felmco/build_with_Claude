# Exercise 03: Batch API Processing

## 🎯 Objective
Advanced implementation of Batch API Processing

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
import time
import anthropic

client = anthropic.Anthropic()

# TODO: build one request per input item, each with a unique custom_id
requests = []

batch = client.messages.batches.create(requests=requests)
while batch.processing_status != "ended":
    time.sleep(30)
    batch = client.messages.batches.retrieve(batch.id)

for entry in client.messages.batches.results(batch.id):
    # TODO: handle entry.result.type: "succeeded", "errored", "canceled", "expired"
    ...
```

## ✅ Expected Output

```
Working system
```

## 🧪 Test Cases

Production tests

## 🎁 Hints

Use `client.messages.batches.create(requests=[{"custom_id": ..., "params": {...}}])`, poll until `processing_status == "ended"`, then iterate `client.messages.batches.results(batch.id)`. Results can arrive in any order, so match them by `custom_id`. Batches are billed at 50% of normal prices.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
# Reference outline: see the Batch Processing lessons in Module 3 for a complete example.
# Handle each result by entry.result.type ("succeeded" -> entry.result.message,
# "errored"/"expired"/"canceled" -> collect the custom_id and resubmit in a new batch).
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
