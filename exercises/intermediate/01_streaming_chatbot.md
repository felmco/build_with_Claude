# Exercise 6: Streaming Chatbot

## 🎯 Objective
Build an interactive chatbot with streaming responses and conversation history management.

## ⏱️ Time
45 minutes

## 📚 Prerequisites
- Completed beginner exercises
- Understanding of streaming responses
- Completed [Module 2: Streaming Basics](../../modules/module2_core_api/04_streaming_basics.md)

## 🎓 Difficulty Level
⭐⭐ Intermediate

## 📝 Instructions

### Part 1: Basic Streaming
Create a chatbot that streams responses in real-time.

**Requirements**:
- Stream responses character by character
- Display text immediately as it arrives
- Show a prompt for user input
- Handle exit commands (quit, exit)

### Part 2: Conversation History
Add conversation history to maintain context.

**Requirements**:
- Store all messages (user and assistant)
- Send history with each new request
- Display conversation number
- Allow reviewing conversation history

### Part 3: Enhanced UX
Add user experience improvements.

**Requirements**:
- Show "thinking" indicator while waiting
- Display token usage after each response
- Add color coding for user vs Claude
- Handle keyboard interrupts gracefully

### Part 4: Save Conversations
Allow users to save conversations to file.

**Requirements**:
- Save on command (/save)
- Include timestamps
- Format nicely
- Confirm save location

## 💻 Starter Code

```python
#!/usr/bin/env python3
"""Exercise 6: Streaming Chatbot"""

from anthropic import Anthropic
from typing import List, Dict

class StreamingChatbot:
    """Interactive streaming chatbot"""

    def __init__(self):
        # TODO: Initialize client and conversation history
        pass

    def chat(self, user_message: str):
        """Send message and stream response"""
        # TODO: Add user message to history
        # TODO: Stream Claude's response
        # TODO: Add response to history
        pass

    def run(self):
        """Run the chatbot loop"""
        # TODO: Implement interactive loop
        pass

def main():
    bot = StreamingChatbot()
    bot.run()

if __name__ == "__main__":
    main()
```

## ✅ Expected Output

```
╔══════════════════════════════════════════════════════════╗
║          Streaming Chatbot with History                  ║
║  Type 'quit' to exit | '/save' to save conversation     ║
╚══════════════════════════════════════════════════════════╝

[Turn 1]
You: Tell me a short story about a robot

Claude: ⏳ Thinking...

Claude: Once upon a time, there was a small cleaning robot named Dusty
who dreamed of exploring space. One day, Dusty was accidentally loaded
onto a spacecraft and got to see the stars after all. Though it meant
leaving Earth forever, Dusty happily cleaned the spacecraft while gazing
at distant galaxies, finally living its dream.

📊 Tokens: 87 | ⏱️  Time: 2.3s

[Turn 2]
You: What was the robot's name?

Claude: ⏳ Thinking...

Claude: The robot's name was Dusty.

📊 Tokens: 12 | ⏱️  Time: 0.5s

[Turn 3]
You: /save

💾 Conversation saved to: conversation_2026-01-14_15-30.txt
```

## 🧪 Test Cases

1. **Test 1**: Basic streaming
   - Input: "Count to 5"
   - Expected: Numbers appear one by one

2. **Test 2**: Context maintenance
   - Input: "My name is Alice"
   - Input: "What's my name?"
   - Expected: "Your name is Alice"

3. **Test 3**: Long response
   - Input: "Write a paragraph about Python"
   - Expected: Text streams smoothly

4. **Test 4**: Interruption
   - Start response, press Ctrl+C
   - Expected: Graceful handling

5. **Test 5**: Save conversation
   - Have a short conversation
   - Type "/save"
   - Expected: File created successfully

## 🎁 Hints

<details>
<summary>Hint 1: Streaming implementation</summary>

```python
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=conversation
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
</details>

<details>
<summary>Hint 2: Managing conversation history</summary>

```python
self.conversation = []

# Add user message
self.conversation.append({
    "role": "user",
    "content": user_message
})

# After streaming, add assistant message
self.conversation.append({
    "role": "assistant",
    "content": response_text
})
```
</details>

<details>
<summary>Hint 3: Error handling</summary>

```python
try:
    ...  # Streaming code
except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted by user")
    return
except Exception as e:
    print(f"\n❌ Error: {e}")
```
</details>

## ✨ Solution

<details>
<summary>Click to view solution</summary>

```python
#!/usr/bin/env python3
"""Exercise 6: Streaming Chatbot - Solution"""

from anthropic import Anthropic
from typing import List, Dict
import time
from datetime import datetime

import anthropic

class StreamingChatbot:
    """Interactive streaming chatbot with history"""

    def __init__(self):
        self.client = Anthropic()
        self.conversation: List[Dict] = []
        self.model = "claude-sonnet-5-5"
        self.turn_count = 0

    def chat(self, user_message: str) -> bool:
        """
        Send message and stream response
        Returns False if special command, True otherwise
        """
        # Handle special commands
        if user_message.lower() in ['quit', 'exit', 'q']:
            return False

        if user_message.startswith('/'):
            self._handle_command(user_message)
            return True

        # Increment turn counter
        self.turn_count += 1

        # Add user message
        self.conversation.append({
            "role": "user",
            "content": user_message
        })

        # Show thinking indicator
        print("\nClaude: ⏳ Thinking...\n")
        time.sleep(0.5)  # Brief pause for effect
        print("\rClaude: ", end="", flush=True)

        # Stream response
        start_time = time.time()
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=1024,
                messages=self.conversation
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)

                # Get final message
                final_message = stream.get_final_message()

            # Calculate stats
            elapsed_time = time.time() - start_time
            output_tokens = final_message.usage.output_tokens

            # Add to history
            self.conversation.append({
                "role": "assistant",
                "content": "".join(
                    b.text for b in final_message.content if b.type == "text"
                )
            })

            # Display stats
            print(f"\n\n📊 Tokens: {output_tokens} | ⏱️  Time: {elapsed_time:.1f}s")

        except KeyboardInterrupt:
            print("\n\n⚠️  Response interrupted by user")
            self._rollback_turn()
        except anthropic.APIError as e:
            print(f"\n❌ Error: {e}")
            self._rollback_turn()

        return True

    def _rollback_turn(self):
        """Drop the unanswered user message so history keeps alternating roles"""
        if self.conversation and self.conversation[-1]["role"] == "user":
            self.conversation.pop()
            self.turn_count -= 1

    def _handle_command(self, command: str):
        """Handle special commands"""
        if command == '/save':
            self._save_conversation()
        elif command == '/history':
            self._show_history()
        elif command == '/clear':
            self.conversation = []
            self.turn_count = 0
            print("✅ Conversation cleared")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: /save, /history, /clear")

    def _save_conversation(self):
        """Save conversation to file"""
        if not self.conversation:
            print("No conversation to save")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"conversation_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("Conversation with Claude\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            for i, msg in enumerate(self.conversation, 1):
                role = "You" if msg["role"] == "user" else "Claude"
                f.write(f"[{i}] {role}: {msg['content']}\n\n")

        print(f"💾 Conversation saved to: {filename}")

    def _show_history(self):
        """Display conversation history"""
        if not self.conversation:
            print("No conversation history")
            return

        print("\n" + "="*60)
        print("Conversation History")
        print("="*60)

        for i, msg in enumerate(self.conversation, 1):
            role = "You" if msg["role"] == "user" else "Claude"
            content = msg["content"]
            # Truncate long messages
            if len(content) > 100:
                content = content[:97] + "..."
            print(f"[{i}] {role}: {content}")

        print("="*60)

    def run(self):
        """Run the chatbot loop"""
        # Header
        print("╔" + "═"*58 + "╗")
        print("║" + " "*10 + "Streaming Chatbot with History" + " "*18 + "║")
        print("║" + "  Type 'quit' to exit | '/save' to save conversation" + " "*3 + "║")
        print("╚" + "═"*58 + "╝")
        print()

        while True:
            try:
                # Get user input
                print(f"\n[Turn {self.turn_count + 1}]")
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Process message
                continue_chat = self.chat(user_input)
                if not continue_chat:
                    print("\nGoodbye! 👋")
                    break

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type 'quit' to exit.")
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Run the chatbot"""
    bot = StreamingChatbot()
    bot.run()

if __name__ == "__main__":
    main()
```
</details>

## 🚀 Extensions

### Extension 1: System Prompts
Add ability to customize Claude's personality with /system command

### Extension 2: Multiple Models
Allow switching between Haiku, Sonnet, and Opus with /model command

### Extension 3: Token Budget
Set a token budget and warn when approaching limit

### Extension 4: Export Formats
Support multiple export formats (JSON, Markdown, HTML)

### Extension 5: Voice Mode
Integrate text-to-speech for Claude's responses

### Extension 6: Web Interface
Build a simple web UI using Flask or Streamlit

## 📖 Learning Outcomes

After completing this exercise, you should understand:
- ✅ How to implement streaming responses
- ✅ How to manage conversation history
- ✅ How to create interactive CLI applications
- ✅ How to handle errors gracefully
- ✅ How to implement special commands
- ✅ File I/O for saving conversations

## 🔗 Related Lessons
- [Streaming Basics](../../modules/module2_core_api/04_streaming_basics.md)
- [Managing Conversations](../../modules/module2_core_api/03_conversations.md)
- [Error Handling](../../modules/module2_core_api/11_error_handling.md)

## 💡 Bonus Challenges

1. **Add Markdown Support**: Render Claude's markdown in the terminal
2. **Implement Undo**: Allow users to undo last message
3. **Add Search**: Search through conversation history
4. **Multi-Session**: Support multiple conversation threads
5. **Add Analytics**: Track and display usage statistics

## 🎉 Completion

Great job! You've built a fully functional streaming chatbot. Next up: [Exercise 7: Image Analysis Tool](./02_image_analysis_tool.md)

---

**Need help?** Review [Streaming Basics](../../modules/module2_core_api/04_streaming_basics.md)
