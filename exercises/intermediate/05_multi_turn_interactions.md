# Exercise 5: Multi-turn Logic

## 🎯 Objective
Create a game of '20 Questions' with Claude.

## ⏱️ Time
45 minutes

## 📚 Prerequisites
- Conversation Management

## 🎓 Difficulty Level
⭐⭐ Intermediate

## 📝 Instructions

### Objective
Script a specific flow:
1. Claude picks an object (you can system prompt this).
2. User asks yes/no questions.
3. Claude answers.
4. End when user guesses correctly.

## 💻 Starter Code

```python
system_prompt = "You are hosting a game of 20 questions. Pick an object (a toaster) and answer yes/no questions."

```

## ✅ Expected Output

```
Interactive game flow.
```

## 🧪 Test Cases

Play the game.

## 🎁 Hints

Use system prompt to enforce rules.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
import anthropic

client = anthropic.Anthropic()
system_prompt = (
    "You are hosting a game of 20 questions. Secretly pick an object (a toaster). "
    "Answer each question only with 'Yes', 'No' or 'Sometimes'. Never reveal the object "
    "unless the player guesses it or has used 20 questions. Count the questions."
)
messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    messages.append({"role": "user", "content": user_input})
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=300,
        system=system_prompt,
        messages=messages,
    )
    reply = "".join(b.text for b in response.content if b.type == "text")
    messages.append({"role": "assistant", "content": reply})
    print(f"Claude: {reply}")
```

Note: the secret object lives only in the system prompt, so the player never sees it. For a different object each game, pick one in your own code and insert it into the prompt.
</details>

## 🚀 Extensions

Have Claude guess YOUR object.

## 📖 Learning Outcomes

- ✅ Guided conversations
- ✅ System instruction adherence

## 🔗 Related Lessons
- [System Prompts](../../modules/module2_core_api/02_system_prompts.md)

## ❓ Common Issues

Claude giving away the answer too early.

## 🎉 Completion

Congratulations! You've completed the exercise.
