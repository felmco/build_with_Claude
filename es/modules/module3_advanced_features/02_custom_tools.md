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

*Nota: Necesitarás escribir o usar un ayudante para convertir modelos Pydantic a JSON Schema para Anthropic.*

## Manejando Subidas de Archivos en Herramientas

Las herramientas no pueden aceptar binarios de archivos directamente en los argumentos JSON. En su lugar:
1. **Sube** el archivo a tu servidor/S3 primero.
2. **Pasa la URL** o ID a la herramienta.

**Definición de Herramienta:**
```json
{
    "name": "analyze_csv",
    "properties": {
        "file_url": {"type": "string", "description": "URL of the CSV file"}
    }
}
```

## Próximos Pasos
- Aprende cómo gestionar [Múltiples Herramientas](./03_multi_tool.md).
