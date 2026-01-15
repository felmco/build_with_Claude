# 2.4 Ejemplos de Código de Gestión de Archivos

*Nota: La API de Archivos está en beta. Debes usar los encabezados beta apropiados.*

## 1. Subiendo un Archivo

```python
import httpx

api_key = "your-api-key"
file_path = "large_document.pdf"

url = "https://api.anthropic.com/v1/files"
headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "anthropic-beta": "files-api-2025-04-14" # Comprueba la documentación para la última cadena beta
}

files = {
    "file": open(file_path, "rb")
}
data = {
    "purpose": "assistants" # o propósito apropiado
}

response = httpx.post(url, headers=headers, files=files, data=data)
file_id = response.json()["id"]
print(f"ID de archivo subido: {file_id}")
```

## 2. Usando un Archivo en un Mensaje

```python
import anthropic

client = anthropic.Anthropic(
    api_key=api_key,
)

# Nota: El soporte beta podría requerir peticiones HTTP crudas o configuración específica del cliente
# dependiendo del soporte de la versión del SDK para la API de Archivos beta.
# A continuación se implica soporte del SDK o envoltorio de la llamada.

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file_id
                    }
                },
                {
                    "type": "text",
                    "text": "Analyze this file."
                }
            ]
        }
    ],
    extra_headers={"anthropic-beta": "files-api-2025-04-14"}
)
```

## 3. Listando y Eliminando

**Listar Archivos:**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: files-api-2025-04-14"
```

**Eliminar Archivo:**
```bash
curl -X DELETE https://api.anthropic.com/v1/files/file_id_here \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: files-api-2025-04-14"
```

## Próximos Pasos
- Avanza a [Fiabilidad y Manejo de Errores](11_manejo_errores.md).
