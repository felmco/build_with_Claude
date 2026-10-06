# Exercise 02: Autonomous Research Agent

## 🎯 Objective
Advanced implementation of Autonomous Research Agent

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
tools = [{"type": "web_search_20260209", "name": "web_search"}]

def research(topic, max_turns=5):
    # TODO: loop calling client.messages.create(model="claude-sonnet-5-5", tools=tools, ...)
    # until stop_reason == "end_turn" (continue on "pause_turn"), then return the final text
    ...
```

## ✅ Expected Output

```
Working system
```

## 🧪 Test Cases

Production tests

## 🎁 Hints

Start from a server-side tool such as `{"type": "web_search_20260209", "name": "web_search"}` and loop until `stop_reason` is `end_turn`. If `stop_reason` is `pause_turn`, send the response content back as the assistant turn to continue. Cap the number of iterations.

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
# Reference outline (see projects/4_research_assistant for the project skeleton):
# messages = [{"role": "user", "content": f"Research {topic} and write a sourced summary."}]
# for _ in range(max_turns):
#     response = client.messages.create(model="claude-sonnet-5-5", max_tokens=4096,
#                                       tools=tools, messages=messages)
#     if response.stop_reason != "pause_turn":
#         break
#     messages.append({"role": "assistant", "content": response.content})
# return "".join(b.text for b in response.content if b.type == "text")
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
