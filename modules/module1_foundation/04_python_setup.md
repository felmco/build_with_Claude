# 1.2 Installing Python and Dependencies

Before working with the Claude API, you need to set up a proper development environment. This guide covers installing Python, setting up a virtual environment, and installing the necessary libraries.

## 1. Install Python

You need **Python 3.7 or higher**.

### Check if Python is installed
Open your terminal or command prompt and run:
```bash
python --version
# OR
python3 --version
```

If you see a version number (e.g., `Python 3.12.0`), you are good to go.
If not, download it from [python.org](https://www.python.org/downloads/).

## 2. Set Up a Project Directory

Create a folder for your project:
```bash
mkdir my_claude_project
cd my_claude_project
```

## 3. Create a Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated from your system Python.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

## 4. Install Dependencies

Install the `anthropic` SDK and `python-dotenv` (for managing API keys securely).

```bash
pip install anthropic python-dotenv
```

## 5. Verify Installation

Create a test script `test_install.py`:

```python
import anthropic
print("Anthropic SDK version:", anthropic.__version__)
```

Run it:
```bash
python test_install.py
```

If it prints the version number without errors, your setup is complete!

## Next Steps
- Learn how to manage your keys in [API Key Management](./06_api_keys.md).
