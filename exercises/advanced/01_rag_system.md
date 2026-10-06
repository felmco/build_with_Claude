# Exercise 01: Build a Simple RAG System

## 🎯 Objective
Advanced implementation of Build a Simple RAG System

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

client = anthropic.Anthropic()

def embed(texts):
    # TODO: call your embeddings provider (e.g. Voyage AI) and return a list of vectors
    ...

def retrieve(question, k=3):
    # TODO: embed the question, rank stored chunks by cosine similarity
    ...

def answer(question):
    # TODO: put the retrieved chunks in the prompt and call client.messages.create(model="claude-sonnet-5-5", ...)
    ...
```

## ✅ Expected Output

```
Working system
```

## 🧪 Test Cases

Production tests

## 🎁 Hints

Anthropic has no embeddings endpoint. Use a third-party provider such as Voyage AI (`pip install voyageai`) to embed chunks and queries, store the vectors (an in-memory list or a vector DB), retrieve the top-k chunks by cosine similarity, and pass them to Claude as context in the prompt.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
# Reference outline (see projects/2_document_qa_system for the project skeleton):
# 1. Split documents into chunks and embed them with a third-party embeddings API.
# 2. Embed the user question the same way and take the top-k chunks by cosine similarity.
# 3. Call client.messages.create(model="claude-sonnet-5-5", max_tokens=1024, ...) with the
#    chunks in <context> tags and an instruction to cite them and say when the answer is missing.
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
