# Exercise 3: Text Generation & Summarization

## 🎯 Objective
Use Claude for common text tasks: summarization, expansion, and rewriting.

## ⏱️ Time
20 minutes

## 📚 Prerequisites
- Basic API knowledge

## 🎓 Difficulty Level
⭐ Beginner

## 📝 Instructions

### Part 1: Summarization
Take a long paragraph of text and ask Claude to summarize it in one sentence.

### Part 2: Tone Adjustment
Ask Claude to rewrite a casual email to be professional.

### Part 3: Extraction
Extract key points (names, dates) from a text.

## 💻 Starter Code

```python
from anthropic import Anthropic

client = Anthropic()

long_text = """
Claude is a family of large language models developed by Anthropic. 
The first model was released in March 2023. Claude models are known 
for their safety and high context window.
"""

def summarize(text):
    # TODO: Ask Claude to summarize
    pass

def make_professional(text):
    # TODO: Ask Claude to rewrite
    pass

def main():
    print(summarize(long_text))

if __name__ == "__main__":
    main()
```

## ✅ Expected Output

```
Summary: Anthropic released the Claude family of safe, high-context AI models starting in March 2023.
```

## 🧪 Test Cases

Check specific output quality.

## 🎁 Hints

<details>
<summary>Hint 1: Prompt Engineering</summary>

Prepare your prompt string by concatenating instructions + text.
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
from anthropic import Anthropic

client = Anthropic()

def ask_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    text = "Hey boss, I ain't coming in today. Sick."
    
    prompt = f"Rewrite the following email to be professional:\n\n{text}"
    print(ask_claude(prompt))

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensions

Try translating text to another language.

## 📖 Learning Outcomes

- ✅ Prompt manipulation
- ✅ Text processing tasks

## 🔗 Related Lessons
- [Prompt Engineering](../../modules/module5_optimization/01_prompt_engineering.md)

## ❓ Common Issues

None

## 🎉 Completion

Congratulations! You've completed the exercise.
