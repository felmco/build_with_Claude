# 1.2 Installing the Anthropic SDK

## Introduction
The Anthropic Python SDK is the official library for interacting with Claude's API. It provides a clean, Pythonic interface with built-in features like error handling, retries, and type hints.

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
pip install anthropic
```

### Method 2: Using pip with specific version

```bash
# Install specific version
pip install anthropic==0.40.0

# Install latest pre-release version
pip install --pre anthropic
```

### Method 3: From source (Advanced)

```bash
git clone https://github.com/anthropics/anthropic-sdk-python.git
cd anthropic-sdk-python
pip install -e .
```

## Setting Up a Virtual Environment

It's highly recommended to use a virtual environment to avoid dependency conflicts.

### Using venv (Standard Library)

```bash
# Create virtual environment
python -m venv claude_env

# Activate on macOS/Linux
source claude_env/bin/activate

# Activate on Windows
claude_env\Scripts\activate

# Install Anthropic SDK
pip install anthropic

# Verify installation
python -c "import anthropic; print(anthropic.__version__)"
```

### Using conda

```bash
# Create conda environment
conda create -n claude_env python=3.11

# Activate environment
conda activate claude_env

# Install SDK
pip install anthropic
```

## Verifying Installation

Create a test file to verify the installation:

**test_installation.py**:
```python
#!/usr/bin/env python3
"""Test script to verify Anthropic SDK installation"""

import sys

def test_import():
    """Test if anthropic package can be imported"""
    try:
        import anthropic
        print(f"✅ Anthropic SDK installed successfully!")
        print(f"   Version: {anthropic.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import anthropic: {e}")
        return False

def test_client_creation():
    """Test if client can be instantiated"""
    try:
        from anthropic import Anthropic

        # This will work even without API key for testing
        client = Anthropic(api_key="test-key")
        print(f"✅ Client instantiation successful!")
        return True
    except Exception as e:
        print(f"❌ Failed to create client: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.7+ required")
        return False

if __name__ == "__main__":
    print("Testing Anthropic SDK Installation\n" + "="*40)

    checks = [
        check_python_version(),
        test_import(),
        test_client_creation()
    ]

    if all(checks):
        print("\n🎉 All checks passed! Ready to use Claude API")
    else:
        print("\n⚠️  Some checks failed. Please review errors above")
```

Run the test:
```bash
python test_installation.py
```

## SDK Features Overview

The Anthropic Python SDK provides:

### 1. Synchronous Client
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 2. Async Client
```python
import asyncio
from anthropic import AsyncAnthropic

async def main():
    client = AsyncAnthropic(api_key="your-api-key")
    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(message.content)

asyncio.run(main())
```

### 3. Streaming Support
```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 4. Type Hints
```python
from anthropic.types import Message, MessageParam

# Full type safety with IDE autocomplete
messages: list[MessageParam] = [
    {"role": "user", "content": "Hello"}
]

response: Message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=messages
)
```

### 5. Built-in Error Handling
```python
from anthropic import (
    APIError,
    APIConnectionError,
    RateLimitError,
    APIStatusError
)

try:
    response = client.messages.create(...)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIConnectionError as e:
    print(f"Connection error: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Additional Dependencies

For specific features, you may need additional packages:

### For Image Processing
```bash
pip install anthropic Pillow
```

### For Async Support
```bash
pip install anthropic httpx[http2]
```

### For Development
```bash
pip install anthropic pytest python-dotenv
```

## Creating a requirements.txt

**requirements.txt**:
```txt
anthropic>=0.40.0
python-dotenv>=1.0.0
httpx[http2]>=0.25.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Common Installation Issues

### Issue 1: SSL Certificate Errors

**Problem**: SSL verification fails
```
SSLError: certificate verify failed
```

**Solution**:
```bash
# Update certifi
pip install --upgrade certifi

# Or use system certificates
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

### Issue 2: Permission Denied

**Problem**: No permission to install globally
```
ERROR: Could not install packages due to an EnvironmentError
```

**Solution**:
```bash
# Use --user flag
pip install --user anthropic

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install anthropic
```

### Issue 3: Version Conflicts

**Problem**: Dependency conflicts with other packages

**Solution**:
```bash
# Create isolated environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install anthropic

# Or specify version constraints
pip install 'anthropic>=0.40.0,<1.0.0'
```

### Issue 4: Import Errors After Installation

**Problem**: `ModuleNotFoundError: No module named 'anthropic'`

**Solution**:
```bash
# Verify you're using the correct Python/pip
which python
which pip

# Check installed packages
pip list | grep anthropic

# Reinstall
pip uninstall anthropic
pip install anthropic
```

## IDE Setup Recommendations

### VS Code
1. Install Python extension
2. Select interpreter from virtual environment
3. Enable type checking:

**settings.json**:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### PyCharm
1. Configure Python interpreter
2. Install Anthropic SDK in project environment
3. Enable type hints inspection

## Quick Start Template

Create a basic project structure:

```bash
mkdir my_claude_project
cd my_claude_project
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install anthropic python-dotenv
```

**project_structure**:
```
my_claude_project/
├── venv/
├── .env
├── requirements.txt
├── main.py
└── README.md
```

**main.py**:
```python
"""Basic Claude API client template"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def main():
    """Main function"""
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    print(message.content[0].text)

if __name__ == "__main__":
    main()
```

## Updating the SDK

Keep your SDK up to date for latest features and bug fixes:

```bash
# Check current version
pip show anthropic

# Update to latest version
pip install --upgrade anthropic

# Update all dependencies
pip install --upgrade -r requirements.txt
```

## Next Steps
- Learn about [API Key Management](./06_api_keys.md)
- Make [Your First API Call](./07_first_api_call.md)

## Additional Resources
- [Official Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [SDK Documentation](https://platform.claude.com/docs/en/sdk/python)
- [PyPI Package](https://pypi.org/project/anthropic/)
