# 1.3 API Key Management

## Introduction
API keys are your credentials for accessing Claude's API. Proper management of API keys is crucial for security and preventing unauthorized access.

## Getting Your API Key

### Step 1: Create an Anthropic Account
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Complete any required verification

### Step 2: Generate an API Key
1. Navigate to **Settings** → **API Keys**
2. Click **Create Key**
3. Give your key a descriptive name (e.g., "Development", "Production")
4. Copy the key immediately (you won't see it again!)
5. Store it securely

## API Key Security Best Practices

### ❌ NEVER Do This
```python
# DON'T hardcode API keys in your code
client = Anthropic(api_key="sk-ant-api03-abc123...")  # BAD!

# DON'T commit API keys to version control
# DON'T share API keys in public repositories
# DON'T log API keys in application logs
# DON'T send API keys in URLs or query parameters
```

### ✅ DO This Instead
```python
# DO use environment variables
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# DO use configuration files (not tracked by git)
# DO rotate keys regularly
# DO use different keys for dev/staging/production
# DO monitor key usage
```

## Method 1: Environment Variables (Recommended)

### On macOS/Linux

**Temporary (current session only)**:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

**Permanent (add to shell config)**:
```bash
# For bash (~/.bashrc or ~/.bash_profile)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For zsh (~/.zshrc)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### On Windows

**PowerShell (temporary)**:
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

**PowerShell (permanent)**:
```powershell
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'your-api-key-here', 'User')
```

**Command Prompt (temporary)**:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### Verifying Environment Variable

```python
import os

# Check if API key is set
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print("✅ API key is set")
    print(f"   Key prefix: {api_key[:10]}...")  # Only show first 10 chars
else:
    print("❌ API key not found")
```

## Method 2: .env File (Development)

### Step 1: Install python-dotenv
```bash
pip install python-dotenv
```

### Step 2: Create .env File

**.env**:
```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL=claude-sonnet-4-5-20250929

# Optional settings
MAX_TOKENS=1024
TEMPERATURE=1.0
```

### Step 3: Add .env to .gitignore

**.gitignore**:
```
# Environment variables
.env
.env.local
.env.*.local

# API keys
*.key
secrets.json
```

### Step 4: Load in Your Code

```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Use other environment variables
model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
max_tokens = int(os.getenv("MAX_TOKENS", "1024"))
```

## Method 3: Configuration Files

### Using JSON Config

**config.json** (add to .gitignore):
```json
{
    "api_key": "your-api-key-here",
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "temperature": 1.0
}
```

**config_loader.py**:
```python
import json
from pathlib import Path
from anthropic import Anthropic

def load_config(config_path: str = "config.json"):
    """Load configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)

def create_client(config_path: str = "config.json"):
    """Create Anthropic client from config file"""
    config = load_config(config_path)
    return Anthropic(api_key=config["api_key"])

# Usage
client = create_client()
```

### Using Python Config Module

**config.py**:
```python
import os

class Config:
    """Application configuration"""

    # API Configuration
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

    # Request Defaults
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "1.0"))

    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")
        return True
```

**main.py**:
```python
from anthropic import Anthropic
from config import Config

# Validate configuration
Config.validate()

# Create client
client = Anthropic(api_key=Config.API_KEY)

# Use configuration
response = client.messages.create(
    model=Config.MODEL,
    max_tokens=Config.MAX_TOKENS,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Method 4: Cloud Secrets Management

### AWS Secrets Manager

```python
import boto3
import json
from anthropic import Anthropic

def get_secret(secret_name: str, region_name: str = "us-east-1"):
    """Retrieve secret from AWS Secrets Manager"""
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
secrets = get_secret("prod/anthropic/api-key")
client = Anthropic(api_key=secrets["api_key"])
```

### Google Cloud Secret Manager

```python
from google.cloud import secretmanager
from anthropic import Anthropic

def get_secret(project_id: str, secret_id: str, version: str = "latest"):
    """Retrieve secret from Google Cloud Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
api_key = get_secret("my-project", "anthropic-api-key")
client = Anthropic(api_key=api_key)
```

### Azure Key Vault

```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from anthropic import Anthropic

def get_secret(vault_url: str, secret_name: str):
    """Retrieve secret from Azure Key Vault"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value

# Usage
api_key = get_secret("https://my-vault.vault.azure.net", "anthropic-api-key")
client = Anthropic(api_key=api_key)
```

## Multiple API Keys Management

### Scenario 1: Multiple Environments

```python
import os
from anthropic import Anthropic

class ClientFactory:
    """Factory for creating environment-specific clients"""

    @staticmethod
    def create(environment: str = "development"):
        """Create client for specific environment"""
        key_map = {
            "development": os.getenv("ANTHROPIC_DEV_KEY"),
            "staging": os.getenv("ANTHROPIC_STAGING_KEY"),
            "production": os.getenv("ANTHROPIC_PROD_KEY")
        }

        api_key = key_map.get(environment)
        if not api_key:
            raise ValueError(f"API key not found for environment: {environment}")

        return Anthropic(api_key=api_key)

# Usage
dev_client = ClientFactory.create("development")
prod_client = ClientFactory.create("production")
```

### Scenario 2: Multiple Projects

**.env**:
```bash
# Project A
PROJECT_A_API_KEY=sk-ant-api03-...

# Project B
PROJECT_B_API_KEY=sk-ant-api03-...
```

```python
import os
from anthropic import Anthropic

# Create clients for different projects
project_a_client = Anthropic(api_key=os.getenv("PROJECT_A_API_KEY"))
project_b_client = Anthropic(api_key=os.getenv("PROJECT_B_API_KEY"))
```

## API Key Rotation

### Why Rotate Keys?
- Security best practice
- Compromised key recovery
- Team member changes
- Compliance requirements

### Rotation Strategy

```python
import os
from datetime import datetime
from anthropic import Anthropic

class RotatingKeyClient:
    """Client with automatic key rotation"""

    def __init__(self):
        self.primary_key = os.getenv("ANTHROPIC_API_KEY_PRIMARY")
        self.secondary_key = os.getenv("ANTHROPIC_API_KEY_SECONDARY")
        self.current_client = Anthropic(api_key=self.primary_key)

    def rotate_key(self):
        """Switch to secondary key"""
        print(f"Rotating to secondary key at {datetime.now()}")
        self.current_client = Anthropic(api_key=self.secondary_key)

    def get_client(self):
        """Get current active client"""
        return self.current_client
```

### Rotation Checklist
1. ✅ Generate new API key in console
2. ✅ Update secondary key in environment
3. ✅ Test secondary key
4. ✅ Switch to secondary key
5. ✅ Revoke old primary key
6. ✅ Update documentation

## Monitoring API Key Usage

### Check Usage Programmatically

```python
from anthropic import Anthropic

client = Anthropic()

# Note: Usage monitoring is typically done via the Console
# This is a placeholder for when the API supports it
def check_usage():
    """Check API usage (via Console currently)"""
    print("Check usage at: https://console.anthropic.com/settings/usage")
```

### Set Up Alerts

1. **Console Alerts**: Configure in Anthropic Console
2. **Custom Monitoring**: Track usage in your application

```python
import logging
from anthropic import Anthropic

class MonitoredClient:
    """Client with usage monitoring"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.request_count = 0
        self.token_count = 0

    def create_message(self, **kwargs):
        """Create message with monitoring"""
        response = self.client.messages.create(**kwargs)

        # Track usage
        self.request_count += 1
        self.token_count += response.usage.input_tokens + response.usage.output_tokens

        logging.info(f"Request #{self.request_count} | Tokens: {self.token_count}")

        return response
```

## Troubleshooting

### Error: Invalid API Key

```python
from anthropic import APIError, AuthenticationError

try:
    client = Anthropic(api_key="invalid-key")
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError as e:
    print("❌ Authentication failed:")
    print("   - Check if API key is correct")
    print("   - Verify key is not expired")
    print("   - Ensure key has proper permissions")
```

### Error: API Key Not Found

```python
import os
from anthropic import Anthropic

# Validate before creating client
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY not found. "
        "Set it using: export ANTHROPIC_API_KEY='your-key'"
    )

client = Anthropic(api_key=api_key)
```

### Best Practice: Validation Function

```python
import os
import sys
from anthropic import Anthropic, AuthenticationError

def validate_api_key() -> str:
    """Validate and return API key"""

    # Check if key exists
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    # Check key format
    if not api_key.startswith("sk-ant-api"):
        print("⚠️  Warning: API key format looks incorrect")
        print("   Keys should start with 'sk-ant-api'")

    # Test key with API call
    try:
        client = Anthropic(api_key=api_key)
        client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )
        print("✅ API key validated successfully")
        return api_key
    except AuthenticationError:
        print("❌ API key validation failed")
        sys.exit(1)

# Use in your application
api_key = validate_api_key()
client = Anthropic(api_key=api_key)
```

## Security Checklist

- ✅ API keys stored in environment variables or secrets manager
- ✅ .env file added to .gitignore
- ✅ No API keys in code or logs
- ✅ Different keys for dev/staging/production
- ✅ Regular key rotation schedule
- ✅ Usage monitoring enabled
- ✅ Team access properly managed
- ✅ Revoked keys for departed team members

## Next Steps
- Make [Your First API Call](./07_first_api_call.md)
- Learn about [Request and Response Handling](./08_request_response.md)

## Additional Resources
- [Anthropic Console](https://console.anthropic.com)
- [API Key Best Practices](https://platform.claude.com/docs/en/security/api-keys)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
