# Exercise 4: Conversation Management

## 🎯 Objective
Maintain a message history list for a coherent chat.

## ⏱️ Time
30 minutes

## 📚 Prerequisites
- Lists in Python

## 🎓 Difficulty Level
⭐⭐ Intermediate

## 📝 Instructions

### Part 1: History List
Create a `messages = []` list.

### Part 2: Appending
Append user message, send to Claude, append assistant response. Repeat.

### Part 3: System Prompt
Add a system prompt to give the assistant a personality.

## 💻 Starter Code

```python
messages = []

while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})
    
    # TODO: Call API with `messages=messages`
    # TODO: Append response to messages
```

## ✅ Expected Output

```
A conversation where Claude remembers name/context.
```

## 🧪 Test Cases

1. My name is Bob. 2. What is my name?

## 🎁 Hints

Always keep the list order correct.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
response = client.messages.create(..., messages=messages)
messages.append({"role": "assistant", "content": response.content[0].text})
```
</details>

## 🚀 Extensions

Implement a 'clear' command to reset history.

## 📖 Learning Outcomes

- ✅ Mental models of context
- ✅ State management

## 🔗 Related Lessons
- [Conversations](../../modules/module2_core_api/03_conversations.md)

## ❓ Common Issues

Context length limit exceeded (need truncation logic).

## 🎉 Completion

Congratulations! You've completed the exercise.
