# 3.1 Building Custom Tools

While simple tools are great, real-world applications often need custom, complex tools.

## Defining Complex Schemas

Tools are defined using [JSON Schema](https://json-schema.org/).

### Nested Objects
```python
{
    "name": "create_user",
    "description": "Create a new user with profile and preferences",
    "input_schema": {
        "type": "object",
        "properties": {
            "profile": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["username", "email"]
            },
            "preferences": {
                "type": "object",
                "properties": {
                    "notifications": {"type": "boolean"},
                    "theme": {"type": "string", "enum": ["light", "dark"]}
                }
            }
        },
        "required": ["profile"]
    }
}
```

## Wrapper Functions

It's best practice to wrap your tools in Python functions or classes that automatically generate the schema. Libraries like Pydantic are great for this.

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str = Field(..., description="The user's username")
    email: str = Field(..., description="User email address")

def create_user(profile: UserProfile):
    # Logic to save to DB
    pass
```

Pydantic v2 can generate the schema for you with `model_json_schema()`:

```python
tool = {
    "name": "create_user",
    "description": "Create a new user",
    "input_schema": {
        "type": "object",
        "properties": {"profile": UserProfile.model_json_schema()},
        "required": ["profile"],
    },
}
```

Pydantic puts nested models under `$defs`; for deeply nested models, inline or hoist those definitions into `input_schema`. Always validate the `input` Claude sends (for example with `UserProfile.model_validate(...)`) before acting on it.

## Handling File Uploads in Tools

Tools can't accept file binaries directly in the JSON arguments. Instead:
1. **Upload** the file to your server/S3 first.
2. **Pass the URL** or ID to the tool.

**Tool Definition:**
```json
{
    "name": "analyze_csv",
    "description": "Analyze a CSV file and return summary statistics",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_url": {"type": "string", "description": "URL of the CSV file"}
        },
        "required": ["file_url"]
    }
}
```

## Next Steps
- Learn how to manage [Multiple Tools](./03_multi_tool.md).
