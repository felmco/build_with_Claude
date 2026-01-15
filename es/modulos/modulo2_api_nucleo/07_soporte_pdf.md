# 2.3 Soporte de PDF

Claude puede leer y analizar nativamente documentos PDF. Esto es parte de sus capacidades multimodales.

## Cómo Funciona

El PDF se convierte internamente en representaciones de imagen/texto. Claude "ve" las páginas del documento.

### Requisitos
- **Formato:** PDF estándar (sin contraseñas/encriptación).
- **Tamaño:** Máx 32MB por petición.
- **Páginas:** Máx 100 páginas por petición (recomendado).

## Enviando un PDF vía API

Envías PDFs de manera similar a las imágenes, usando un bloque `document` con codificación Base64.

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Codificar PDF
with open("report.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

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
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize the key findings in this report."
                }
            ]
        }
    ]
)
print(message.content[0].text)
```

## Optimizando el Rendimiento con PDF

1. **Selección de Texto:** Asegúrate de que el PDF tenga texto seleccionable si es posible (aunque Claude usa visión, las capas de texto ayudan).
2. **Fragmentación (Chunking):** Para documentos muy grandes (>100 páginas), divide el PDF en fragmentos más pequeños o múltiples peticiones.
3. **Prompting:** Haz preguntas específicas. "Encuentra la tabla en la página 3 y extrae las cifras de ingresos."

## Próximos Pasos
- Aprende más sobre [Estrategias de Análisis de Documentos](08_analisis_documentos.md).
