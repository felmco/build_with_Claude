# Exercise 2: Simple Chatbot

## 🎯 Objective
Build an interactive loop that allows continuous conversation with Claude.

## ⏱️ Time
20 minutes

## 📚 Prerequisites
- Python 3.7+ installed
- Anthropic SDK installed
- API key configured

## 🎓 Difficulty Level
⭐ Beginner

## 📝 Instructions

### Part 1: The Loop
Create a `while True` loop that continuously asks for user input.

### Part 2: Sending Messages
Send the user's input to Claude and print the response.

### Part 3: Exit Condition
Allow the user to type 'quit' or 'exit' to end the program cleanly.

### Part 4: Context (Optional for now)
For this strict beginner exercise, you don't need to maintain history (we'll do that in Intermediate), but try to notice that Claude doesn't remember previous messages in this simple loop implementation.

## 💻 Starter Code

```python
import os
from anthropic import Anthropic

client = Anthropic()

def main():
    print("Simple Chatbot (type 'quit' to exit)")
    
    while True:
        # TODO: Get user input
        
        # TODO: Check for exit condition
        
        # TODO: Send message to Claude
        
        # TODO: Print response
        pass

if __name__ == "__main__":
    main()
```

## ✅ Expected Output

```
Simple Chatbot (type 'quit' to exit)
You: Hi there!
Claude: Hello! How can I help you today?
You: quit
Goodbye!
```

## 🧪 Test Cases

1. **Test 1**: Basic conversation
   - Input: "Hello"
   - Expected: Response from Claude

2. **Test 2**: Exit
   - Input: "quit"
   - Expected: Program terminates

## 🎁 Hints

<details>
<summary>Hint 1: Loop structure</summary>

Use `while True:` and `input()`.
</details>
<details>
<summary>Hint 2: Exit check</summary>

Use `if user_input.lower() == 'quit': break`
</details>


## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
import os
from anthropic import Anthropic

def main():
    client = Anthropic()
    print("Chatbot initialized. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            print(f"Claude: {message.content[0].text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensions

1. Add a system prompt to give the bot a persona (e.g., a pirate).
2. Add color to the output.

## 📖 Learning Outcomes

- ✅ Building interactive loops
- ✅ Handling user input
- ✅ Basic error handling in loops

## 🔗 Related Lessons
- [First API Call](../../modules/module1_foundation/07_first_api_call.md)

## ❓ Common Issues

### Issue 1: Endless Loop
If you forget the break statement, you can't exit. Use Ctrl+C to force quit.

## 🎉 Completion

Congratulations! You've completed the exercise.
