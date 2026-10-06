# 3.1 Construyendo Herramientas Personalizadas

Aunque las herramientas simples son geniales, las aplicaciones del mundo real a menudo necesitan herramientas personalizadas y complejas.

## Definiendo Esquemas Complejos

Las herramientas se definen usando [JSON Schema](https://json-schema.org/).

### Objetos Anidados
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

## Funciones Envoltorio (Wrapper Functions)

Una mejor práctica es envolver tus herramientas en funciones o clases de Python que generen automáticamente el esquema. Librerías como Pydantic son geniales para esto.

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str = Field(..., description="The user's username")
    email: str = Field(..., description="User email address")

def create_user(profile: UserProfile):
    # Lógica para guardar en DB
    pass
```

Pydantic v2 puede generar el esquema por ti con `model_json_schema()`:

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

Pydantic coloca los modelos anidados bajo `$defs`; para modelos con mucho anidamiento, incorpora esas definiciones en línea o súbelas al nivel de `input_schema`. Valida siempre el `input` que envía Claude (por ejemplo con `UserProfile.model_validate(...)`) antes de actuar sobre él.

## Manejando Subidas de Archivos en Herramientas

Las herramientas no pueden aceptar binarios de archivos directamente en los argumentos JSON. En su lugar:
1. **Sube** el archivo a tu servidor/S3 primero.
2. **Pasa la URL** o ID a la herramienta.

**Definición de Herramienta:**
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

## Próximos Pasos
- Aprende cómo gestionar [Múltiples Herramientas](03_multi_herramienta.md).
