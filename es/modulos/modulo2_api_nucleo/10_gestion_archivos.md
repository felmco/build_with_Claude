# 2.4 Ejemplos de Código de Gestión de Archivos

*Nota: La API de Archivos está disponible de forma general: no necesita cabecera beta y el SDK la expone como `client.files`. Consulta la [documentación de la API de Archivos](https://platform.claude.com/docs/en/build-with-claude/files).*

## 1. Subiendo un Archivo

```python
import anthropic

client = anthropic.Anthropic()

with open("large_document.pdf", "rb") as f:
    uploaded = client.files.upload(file=("large_document.pdf", f, "application/pdf"))

file_id = uploaded.id
print(f"ID del archivo subido: {file_id}")
```

## 2. Usando un Archivo en un Mensaje

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "file", "file_id": file_id}},
                {"type": "text", "text": "Analiza este archivo."},
            ],
        }
    ],
)
print(message.content[0].text)
```

El tipo de bloque debe coincidir con el archivo: `document` para PDF/texto, `image` para imágenes.

## 3. Listando y Eliminando

**Listar Archivos:**
```bash
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

**Eliminar Archivo:**
```bash
curl -X DELETE https://api.anthropic.com/v1/files/file_id_here \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

O con el SDK:

```python
for f in client.files.list():  # pagina automáticamente
    print(f.id, f.filename, f.size_bytes)

client.files.delete(file_id)
```

Los archivos subidos permanecen en el almacenamiento de tu organización hasta que los elimines.

## Próximos Pasos
- Avanza a [Fiabilidad y Manejo de Errores](11_manejo_errores.md).
