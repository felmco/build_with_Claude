# 2.1 Messages API Fundamentals

## Introduction
The Messages API is the primary interface for interacting with Claude. This lesson covers all essential features and best practices for using the Messages API effectively.

## Basic Message Structure

### Minimal Request
```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Full Request with All Parameters
```python
message = client.messages.create(
    # Required parameters
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],

    # Optional parameters
    system="You are a physics professor explaining concepts simply.",
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    metadata={"user_id": "user_123"},
    stop_sequences=["Human:", "Assistant:"]
)
```

## Understanding Message Roles

### User Messages
Messages from the user to Claude:

```python
messages = [
    {
        "role": "user",
        "content": "What's the weather like?"
    }
]
```

### Assistant Messages
Messages from Claude (used for conversation history):

```python
messages = [
    {
        "role": "user",
        "content": "What's the capital of France?"
    },
    {
        "role": "assistant",
        "content": "The capital of France is Paris."
    },
    {
        "role": "user",
        "content": "What's its population?"
    }
]
```

### Rules for Message Roles
1. ✅ Must start with a user message
2. ✅ Must alternate between user and assistant
3. ✅ Must end with a user message
4. ❌ Cannot have two consecutive user messages
5. ❌ Cannot have two consecutive assistant messages

**Valid**:
```python
messages = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "How are you?"}
]  # ✅ Valid: alternating roles, ends with user
```

**Invalid**:
```python
messages = [
    {"role": "user", "content": "Hi"},
    {"role": "user", "content": "Hello?"}  # ❌ Two consecutive user messages
]

messages = [
    {"role": "assistant", "content": "Hello!"}  # ❌ Starts with assistant
]
```

## Content Types

### Text Content (Simple)
```python
messages = [
    {
        "role": "user",
        "content": "This is simple text content"
    }
]
```

### Text Content (Structured)
```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Analyze this data and provide insights"
            }
        ]
    }
]
```

### Multimodal Content (Text + Images)
```python
import base64

# Read image file
with open("image.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            }
        ]
    }
]
```

## System Prompts

System prompts provide instructions and context for Claude's behavior:

### Basic System Prompt
```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[
        {"role": "user", "content": "How do I read a file in Python?"}
    ]
)
```

### Advanced System Prompt with Multiple Sections
```python
system_prompt = """You are an expert Python tutor with the following characteristics:

ROLE:
- Patient and encouraging teacher
- Focus on best practices and clean code
- Provide working examples

STYLE:
- Use simple, clear language
- Break down complex concepts
- Include code comments
- Suggest next steps for learning

CONSTRAINTS:
- Always provide complete, runnable code
- Include error handling in examples
- Mention Python version compatibility
- Cite official documentation when relevant
"""

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "Teach me about decorators"}
    ]
)
```

## Request Parameters Deep Dive

### max_tokens
Maximum number of tokens in the response:

```python
# Short response (50-100 tokens ≈ 40-75 words)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Summarize Python in one paragraph"}]
)

# Medium response (1000-2000 tokens ≈ 750-1500 words)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2000,
    messages=[{"role": "user", "content": "Explain OOP in Python"}]
)

# Long response (4000+ tokens ≈ 3000+ words)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a detailed tutorial on async Python"}]
)
```

**Token Guidelines**:
- 1 token ≈ 0.75 English words
- Maximum: 8,192 tokens (varies by model)
- Set based on expected response length
- Consider cost (charged per output token)

### temperature
Controls randomness and creativity (0.0 - 1.0):

```python
# Deterministic responses (factual, consistent)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=0.0,  # Most deterministic
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

# Balanced responses (default behavior)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=0.7,  # Balanced
    messages=[{"role": "user", "content": "Explain machine learning"}]
)

# Creative responses (varied, imaginative)
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=1.0,  # Most creative
    messages=[{"role": "user", "content": "Write a creative story"}]
)
```

**Temperature Guidelines**:
| Temperature | Best For | Example Use Cases |
|-------------|----------|-------------------|
| 0.0 - 0.3 | Factual, deterministic | Math, code generation, Q&A |
| 0.4 - 0.7 | Balanced | General chat, analysis |
| 0.8 - 1.0 | Creative | Story writing, brainstorming |

### top_p (Nucleus Sampling)
Alternative to temperature for controlling randomness:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    top_p=0.9,  # Consider top 90% probability mass
    messages=[{"role": "user", "content": "Generate ideas"}]
)
```

**Guidelines**:
- Range: 0.0 - 1.0
- Lower values = more focused
- Higher values = more diverse
- Use either `temperature` OR `top_p`, not both

### top_k
Limits vocabulary to top K tokens:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    top_k=40,  # Consider only top 40 tokens at each step
    messages=[{"role": "user", "content": "Tell me about AI"}]
)
```

### stop_sequences
Stop generation when certain sequences are encountered:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    stop_sequences=["</end>", "STOP", "\n\n---"],
    messages=[{"role": "user", "content": "List 5 programming languages"}]
)
```

**Use Cases**:
- Stop at specific markers
- Limit list lengths
- Control output format
- Implement custom protocols

### metadata
Attach custom metadata for tracking:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    metadata={
        "user_id": "user_12345",
        "session_id": "session_abc",
        "environment": "production"
    },
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Response Structure

### Basic Response Fields
```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# Response fields
print(f"ID: {message.id}")                    # Unique message ID
print(f"Type: {message.type}")                # Always "message"
print(f"Role: {message.role}")                # Always "assistant"
print(f"Model: {message.model}")              # Model used
print(f"Content: {message.content}")          # List of content blocks
print(f"Stop Reason: {message.stop_reason}")  # Why generation stopped
print(f"Stop Sequence: {message.stop_sequence}")  # If stopped by sequence
print(f"Usage: {message.usage}")              # Token usage info
```

### Content Blocks
```python
# Single text block (most common)
message.content[0].type  # "text"
message.content[0].text  # The actual response text

# Multiple content blocks (less common)
for block in message.content:
    if block.type == "text":
        print(f"Text: {block.text}")
```

### Token Usage
```python
# Detailed usage information
usage = message.usage

print(f"Input tokens: {usage.input_tokens}")
print(f"Output tokens: {usage.output_tokens}")
print(f"Total tokens: {usage.input_tokens + usage.output_tokens}")

# Calculate approximate cost (example rates)
INPUT_COST_PER_MTK = 0.003  # Per million tokens
OUTPUT_COST_PER_MTK = 0.015  # Per million tokens

input_cost = (usage.input_tokens / 1_000_000) * INPUT_COST_PER_MTK
output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_COST_PER_MTK
total_cost = input_cost + output_cost

print(f"Estimated cost: ${total_cost:.6f}")
```

### Stop Reasons
```python
stop_reason = message.stop_reason

# Possible values:
# - "end_turn": Natural completion
# - "max_tokens": Reached max_tokens limit
# - "stop_sequence": Hit a stop sequence
# - "tool_use": Model wants to use a tool (advanced feature)

if stop_reason == "max_tokens":
    print("⚠️  Response truncated - increase max_tokens")
elif stop_reason == "end_turn":
    print("✅ Complete response")
elif stop_reason == "stop_sequence":
    print(f"🛑 Stopped at sequence: {message.stop_sequence}")
```

## Complete Example: Structured API Call

**structured_api_call.py**:
```python
#!/usr/bin/env python3
"""Complete example of structured Messages API usage"""

from anthropic import Anthropic
from typing import Dict, List, Optional
import os

class ClaudeClient:
    """Wrapper for Claude Messages API"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"

    def send_message(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Send a message to Claude and return structured response

        Args:
            prompt: User message
            system: System prompt (optional)
            max_tokens: Maximum response tokens
            temperature: Response randomness (0.0-1.0)
            conversation_history: Previous messages (optional)

        Returns:
            Dict with response text, usage, and metadata
        """
        # Build messages list
        messages = conversation_history or []
        messages.append({"role": "user", "content": prompt})

        # Create API request
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system:
            params["system"] = system

        # Make API call
        message = self.client.messages.create(**params)

        # Return structured response
        return {
            "text": message.content[0].text,
            "id": message.id,
            "model": message.model,
            "stop_reason": message.stop_reason,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "total_tokens": message.usage.input_tokens + message.usage.output_tokens
            }
        }

def main():
    """Example usage"""
    client = ClaudeClient()

    # Simple request
    response = client.send_message(
        prompt="Explain Python decorators in 2 sentences",
        system="You are a Python expert. Be concise."
    )

    print("Response:")
    print(response["text"])
    print(f"\nTokens used: {response['usage']['total_tokens']}")

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Start Simple, Then Optimize
```python
# Start with defaults
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

# Optimize based on needs
# - Adjust max_tokens for response length
# - Set temperature for desired creativity
# - Add system prompts for behavior control
```

### 2. Always Handle Token Limits
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

if response.stop_reason == "max_tokens":
    print("Warning: Response may be incomplete")
    # Consider increasing max_tokens or splitting the request
```

### 3. Use System Prompts Effectively
```python
# ❌ Don't put instructions in user message
messages = [
    {"role": "user", "content": "You are a teacher. Explain photosynthesis."}
]

# ✅ Use system prompt for instructions
system = "You are an experienced biology teacher."
messages = [
    {"role": "user", "content": "Explain photosynthesis."}
]
```

### 4. Structure Multi-Turn Conversations Properly
```python
# Maintain conversation history
conversation = []

# Turn 1
conversation.append({"role": "user", "content": "What's Python?"})
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=conversation
)
conversation.append({"role": "assistant", "content": response.content[0].text})

# Turn 2 (with context)
conversation.append({"role": "user", "content": "What are its main uses?"})
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=conversation
)
```

## Next Steps
- Learn about [System Prompts](./02_system_prompts.md)
- Explore [Managing Conversations](./03_conversations.md)
- Try [Streaming Responses](./04_streaming_basics.md)

## Additional Resources
- [Official Messages API Documentation](https://platform.claude.com/docs/en/api/messages)
- [API Reference](https://platform.claude.com/docs/en/api/overview)
- [Best Practices Guide](https://platform.claude.com/docs/en/build-with-claude/best-practices)
