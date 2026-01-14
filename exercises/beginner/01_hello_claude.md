# Exercise 1: Hello Claude

## 🎯 Objective
Make your first API call to Claude and display a formatted response.

## ⏱️ Time
15 minutes

## 📚 Prerequisites
- Python 3.7+ installed
- Anthropic SDK installed
- API key configured
- Completed [Module 1: First API Call](../../modules/module1_foundation/07_first_api_call.md)

## 🎓 Difficulty Level
⭐ Beginner

## 📝 Instructions

### Part 1: Basic Hello
Create a script that sends "Hello, Claude!" and prints the response.

**Requirements**:
- Initialize Anthropic client
- Send a simple message
- Print the response
- Include basic error handling

### Part 2: Formatted Output
Enhance your script to display:
- A header
- The user's question
- Claude's response
- Token usage information

### Part 3: Multiple Questions
Ask Claude three different questions and display all responses nicely formatted.

## 💻 Starter Code

```python
#!/usr/bin/env python3
"""Exercise 1: Hello Claude"""

from anthropic import Anthropic

def main():
    # TODO: Initialize the client

    # TODO: Send a message to Claude

    # TODO: Print the response

    pass

if __name__ == "__main__":
    main()
```

## ✅ Expected Output

```
═══════════════════════════════════════
Exercise 1: Hello Claude
═══════════════════════════════════════

You: Hello, Claude!

Claude: Hello! I'm Claude, an AI assistant created by Anthropic.
How can I help you today?

📊 Usage:
   Input tokens: 12
   Output tokens: 25
   Total tokens: 37
```

## 🧪 Test Cases

1. **Test 1**: Basic greeting
   - Input: "Hello, Claude!"
   - Expected: Friendly greeting response

2. **Test 2**: Question
   - Input: "What is 2 + 2?"
   - Expected: "4" or "2 + 2 equals 4"

3. **Test 3**: Creative request
   - Input: "Tell me a one-sentence joke"
   - Expected: A short joke

## 🎁 Hints

<details>
<summary>Hint 1: Initializing the client</summary>

```python
from anthropic import Anthropic
client = Anthropic()  # Uses ANTHROPIC_API_KEY env var
```
</details>

<details>
<summary>Hint 2: Making an API call</summary>

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Your message here"}
    ]
)
```
</details>

<details>
<summary>Hint 3: Accessing the response</summary>

```python
response_text = message.content[0].text
print(response_text)
```
</details>

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
#!/usr/bin/env python3
"""Exercise 1: Hello Claude - Solution"""

from anthropic import Anthropic
import os

def send_message(client, user_message: str):
    """Send a message to Claude and return response"""
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return message

def display_response(user_message: str, message):
    """Display formatted response"""
    print(f"\nYou: {user_message}\n")
    print(f"Claude: {message.content[0].text}\n")
    print("📊 Usage:")
    print(f"   Input tokens: {message.usage.input_tokens}")
    print(f"   Output tokens: {message.usage.output_tokens}")
    print(f"   Total tokens: {message.usage.input_tokens + message.usage.output_tokens}")

def main():
    """Main function"""
    # Header
    print("═" * 60)
    print("Exercise 1: Hello Claude")
    print("═" * 60)

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Please set ANTHROPIC_API_KEY environment variable")
        return

    # Initialize client
    client = Anthropic()

    # Part 1: Basic Hello
    user_message = "Hello, Claude!"
    message = send_message(client, user_message)
    display_response(user_message, message)

    # Part 3: Multiple questions
    questions = [
        "What is 2 + 2?",
        "Tell me a one-sentence joke",
        "What is the capital of France?"
    ]

    print("\n" + "═" * 60)
    print("Multiple Questions")
    print("═" * 60)

    for question in questions:
        message = send_message(client, question)
        display_response(question, message)
        print("-" * 60)

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensions

Once you've completed the basic exercise, try these extensions:

### Extension 1: Interactive Mode
Make the script interactive - keep asking for user input until they type 'quit'

```python
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'quit':
        break
    # Send to Claude and display response
```

### Extension 2: Save Conversation
Save the conversation to a text file

### Extension 3: Add Colors
Use the `colorama` library to add colors to output

### Extension 4: Time the Responses
Measure and display how long each response takes

### Extension 5: Compare Models
Send the same question to different models (Haiku, Sonnet, Opus) and compare

## 📖 Learning Outcomes

After completing this exercise, you should understand:
- ✅ How to initialize the Anthropic client
- ✅ How to make a basic API call
- ✅ How to access response content
- ✅ How to check token usage
- ✅ Basic error handling

## 🔗 Related Lessons
- [First API Call](../../modules/module1_foundation/07_first_api_call.md)
- [Request and Response](../../modules/module1_foundation/08_request_response.md)
- [Messages API](../../modules/module2_core_api/01_messages_api.md)

## ❓ Common Issues

### Issue 1: API Key Not Found
**Error**: `ANTHROPIC_API_KEY not found`

**Solution**:
```bash
export ANTHROPIC_API_KEY='your-api-key'
```

### Issue 2: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'anthropic'`

**Solution**:
```bash
pip install anthropic
```

### Issue 3: Attribute Error
**Error**: `AttributeError: 'Message' object has no attribute 'content'`

**Solution**: Make sure you're accessing `message.content[0].text`, not just `message.content`

## 🎉 Completion

Congratulations! You've completed your first exercise. Move on to [Exercise 2: Temperature Experiments](./02_temperature.md)

---

**Need help?** Review [Module 1: First API Call](../../modules/module1_foundation/07_first_api_call.md)
