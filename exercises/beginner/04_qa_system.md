# Exercise 4: Context-based Q&A

## 🎯 Objective
Build a system that answers questions based ONLY on provided text context.

## ⏱️ Time
25 minutes

## 📚 Prerequisites
- String formatting

## 🎓 Difficulty Level
⭐ Beginner

## 📝 Instructions

### Part 1: The Context
Define a string variable containing some specific information (e.g., a mini-policy doc).

### Part 2: The Prompt
Construct a prompt that injects this context and instructs Claude to answer user questions using only that context.

## 💻 Starter Code

```python
context = """
The return policy allows returns within 30 days. 
Receipt is required. Refunds take 5-7 business days.
"""

question = "Can I return without a receipt?"

# TODO: Construct prompt with context and question
```

## ✅ Expected Output

```
No, a receipt is required for returns.
```

## 🧪 Test Cases

Ask about something not in text -> Should say 'I don't know'.

## 🎁 Hints

<details>
<summary>Hint 1: XML Tags</summary>

Use <context> tags to delimit the text.
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
prompt = f"""
Answer the question based only on the following context:

<context>
{context}
</context>

Question: {question}
"""

```
</details>

## 🚀 Extensions

Load context from a file.

## 📖 Learning Outcomes

- ✅ Context injection
- ✅ Grounding answers

## 🔗 Related Lessons
- [Prompt Engineering](../../modules/module5_optimization/01_prompt_engineering.md)

## ❓ Common Issues

Model using outside knowledge? Add 'Answer only using the provided text'.

## 🎉 Completion

Congratulations! You've completed the exercise.
