# 1.4 Your First API Call

## Introduction
This guide walks you through making your first API call to Claude. By the end, you'll have sent a message to Claude and received a response!

## Prerequisites
- ✅ Python 3.7+ installed
- ✅ Anthropic SDK installed (`pip install anthropic`)
- ✅ API key configured (see [API Key Management](./06_api_keys.md))

## The Simplest Possible Example

**hello_claude.py**:
```python
from anthropic import Anthropic

# Initialize the client
client = Anthropic()  # Uses ANTHROPIC_API_KEY environment variable

# Make your first API call
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude! Introduce yourself in one sentence."}
    ]
)

# Print the response
print(message.content[0].text)
```

Run it:
```bash
python hello_claude.py
```

**Expected Output**:
```
I'm Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest.
```

🎉 Congratulations! You've just made your first API call to Claude!

## Understanding the Code

Let's break down each part:

### 1. Import and Initialize

```python
from anthropic import Anthropic

client = Anthropic()  # Automatically uses ANTHROPIC_API_KEY env var
```

The `Anthropic()` client:
- Looks for `ANTHROPIC_API_KEY` environment variable
- Sets up authentication
- Provides methods to interact with the API

### 2. Create a Message

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",  # Which model to use
    max_tokens=1024,                      # Maximum response length
    messages=[                            # Conversation history
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
```

**Parameters explained**:
- `model`: Which Claude model to use (Sonnet 4.5 recommended)
- `max_tokens`: Maximum tokens in response (1 token ≈ 0.75 words)
- `messages`: List of messages in the conversation

### 3. Access the Response

```python
print(message.content[0].text)
```

The response is a `Message` object with:
- `content`: List of content blocks
- `content[0].text`: The actual text response
- `usage`: Token usage information
- `model`: Model that generated the response

## Complete Example with Error Handling

**robust_example.py**:
```python
#!/usr/bin/env python3
"""A robust first API call example with error handling"""

import os
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError

def make_api_call():
    """Make an API call to Claude with error handling"""

    # Check if API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it using: export ANTHROPIC_API_KEY='your-api-key'")
        return

    try:
        # Initialize client
        print("🔄 Initializing client...")
        client = Anthropic()

        # Make API call
        print("📤 Sending message to Claude...")
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude! Introduce yourself in one sentence."
                }
            ]
        )

        # Display response
        print("\n✅ Response received!")
        print("─" * 50)
        print(message.content[0].text)
        print("─" * 50)

        # Display usage information
        print(f"\n📊 Usage:")
        print(f"   Input tokens: {message.usage.input_tokens}")
        print(f"   Output tokens: {message.usage.output_tokens}")
        print(f"   Total tokens: {message.usage.input_tokens + message.usage.output_tokens}")

    except RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        print("   Try again in a few moments")

    except APIConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("   Check your internet connection")

    except APIError as e:
        print(f"❌ API error: {e}")
        print("   Check API status: https://status.anthropic.com")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    make_api_call()
```

## Interactive Example

Create an interactive script that takes user input:

**interactive_claude.py**:
```python
#!/usr/bin/env python3
"""Interactive Claude conversation"""

import os
from anthropic import Anthropic

def main():
    """Run interactive conversation with Claude"""

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    client = Anthropic()

    print("Interactive Claude Chat")
    print("Type 'quit' to exit\n")
    print("─" * 50)

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Make API call
            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            # Display response
            print(f"\nClaude: {message.content[0].text}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python interactive_claude.py
```

Example interaction:
```
Interactive Claude Chat
Type 'quit' to exit
──────────────────────────────────────────────────

You: What's 25 * 4?

Claude: 25 * 4 = 100

You: Explain how photosynthesis works

Claude: Photosynthesis is the process by which plants convert light energy...

You: quit
Goodbye!
```

## Understanding Response Structure

The `Message` object contains several important fields:

```python
message = client.messages.create(...)

# Main response text
text = message.content[0].text

# Message metadata
message_id = message.id              # Unique message ID
model_used = message.model           # Model that generated response
role = message.role                  # Always "assistant"

# Token usage
input_tokens = message.usage.input_tokens
output_tokens = message.usage.output_tokens

# Stop reason
stop_reason = message.stop_reason  # Why generation stopped

print(f"Message ID: {message_id}")
print(f"Model: {model_used}")
print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Stop reason: {stop_reason}")
print(f"\nResponse:\n{text}")
```

**Output**:
```
Message ID: msg_01ABC123XYZ...
Model: claude-sonnet-4-5-20250929
Input tokens: 15
Output tokens: 25
Stop reason: end_turn

Response:
I'm Claude, an AI assistant created by Anthropic.
```

## Common Parameters

### max_tokens
Controls maximum response length:

```python
# Short response
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=50,  # Very short
    messages=[{"role": "user", "content": "Write a story"}]
)

# Long response
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,  # Much longer
    messages=[{"role": "user", "content": "Write a detailed story"}]
)
```

**Guidelines**:
- Minimum: 1 token
- Maximum: 8,192 tokens (model-specific)
- 1 token ≈ 0.75 English words
- Set based on expected response length

### temperature
Controls randomness (0.0 to 1.0):

```python
# More focused and deterministic
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=0.0,  # Most deterministic
    messages=[{"role": "user", "content": "What is 2+2?"}]
)

# More creative and varied
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=1.0,  # Most creative
    messages=[{"role": "user", "content": "Write a creative story"}]
)
```

**Guidelines**:
- 0.0: Deterministic, consistent responses
- 0.5-0.7: Balanced (default: 1.0)
- 1.0: More creative, varied responses
- Use low temperature for factual tasks
- Use higher temperature for creative tasks

### system
Provide instructions to Claude:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful Python tutor. Explain concepts simply with examples.",
    messages=[
        {"role": "user", "content": "What are list comprehensions?"}
    ]
)
```

## Testing Different Models

**model_comparison.py**:
```python
from anthropic import Anthropic

client = Anthropic()
prompt = "Explain quantum computing in one sentence."

models = {
    "Haiku 3.5": "claude-3-5-haiku-20241022",
    "Sonnet 4.5": "claude-sonnet-4-5-20250929",
    "Opus 4.5": "claude-opus-4-5-20251101"
}

print("Comparing Models")
print("=" * 60)

for name, model_id in models.items():
    print(f"\n{name}:")
    print("-" * 60)

    message = client.messages.create(
        model=model_id,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    print(message.content[0].text)
    print(f"Tokens: {message.usage.output_tokens}")
```

## Putting It All Together: Complete Template

**claude_template.py**:
```python
#!/usr/bin/env python3
"""Complete template for Claude API calls"""

import os
import sys
from anthropic import Anthropic, APIError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_environment():
    """Validate required environment variables"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

def create_client():
    """Create and return Anthropic client"""
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def send_message(client, prompt: str, system: str = None):
    """Send a message to Claude and return response"""
    try:
        params = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system:
            params["system"] = system

        message = client.messages.create(**params)
        return message.content[0].text

    except APIError as e:
        print(f"API Error: {e}")
        return None

def main():
    """Main function"""
    validate_environment()
    client = create_client()

    # Example usage
    response = send_message(
        client,
        prompt="What is the capital of France?",
        system="You are a geography expert. Be concise."
    )

    if response:
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
```

## Common First-Time Issues

### Issue 1: API Key Not Found
```
Error: ANTHROPIC_API_KEY not set
```
**Solution**: Set environment variable:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### Issue 2: Import Error
```
ModuleNotFoundError: No module named 'anthropic'
```
**Solution**: Install SDK:
```bash
pip install anthropic
```

### Issue 3: Invalid API Key
```
AuthenticationError: Invalid API key
```
**Solution**: Check your API key:
- Verify it starts with `sk-ant-api`
- Check for extra spaces or quotes
- Regenerate key in console if needed

### Issue 4: Rate Limiting
```
RateLimitError: 429 Too Many Requests
```
**Solution**: Add retry logic or slow down requests

## Quick Reference

```python
# Minimal example
from anthropic import Anthropic

client = Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

## Next Steps
- Learn about [Request and Response Handling](./08_request_response.md)
- Explore [Error Handling](./09_error_handling.md)
- Try [Module 2: Core API Features](../module2_core_api/README.md)

## Practice Exercises

1. **Hello World**: Make a simple API call
2. **Calculator**: Ask Claude to solve math problems
3. **Translator**: Translate text between languages
4. **Code Helper**: Ask for coding help
5. **Creative Writing**: Generate a short story

Try these on your own to practice!

## Additional Resources
- [Official API Reference](https://platform.claude.com/docs/en/api/messages)
- [Python SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
- [Example Code Repository](https://github.com/anthropics/anthropic-quickstarts)
