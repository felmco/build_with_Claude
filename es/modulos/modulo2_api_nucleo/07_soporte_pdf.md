# 2.3 Soporte de PDF

Claude puede leer y analizar nativamente documentos PDF. Esto es parte de sus capacidades multimodales.

## Cómo Funciona

Claude extrae el texto de cada página y además ve cada página como una imagen, así que puede leer gráficos, tablas y contenido escaneado.

### Requisitos
- **Formato:** PDF estándar (sin contraseñas/encriptación).
- **Tamaño:** Máx 32MB por petición (toda la carga útil, no solo el PDF).
- **Páginas:** Máx 600 páginas por petición en modelos con ventana de contexto de 1M tokens (100 páginas en Haiku 4.5, que tiene 200K).
- **Coste:** Cada página cuesta tokens de texto más tokens de imagen, así que los PDF largos se acumulan rápido; usa `client.messages.count_tokens` para comprobarlo.

## Enviando un PDF vía API

Envías PDFs de manera similar a las imágenes, usando un bloque `document` con una fuente base64, `url` o de la API de Archivos (`file`).

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Codificar PDF
with open("report.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-5-5",
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

Para un PDF en una URL pública, usa `"source": {"type": "url", "url": "https://example.com/report.pdf"}`. Para un PDF que consultarás muchas veces, súbelo una vez con la [API de Archivos](09_api_archivos.md) y refiérelo por `file_id`.

## Optimizando el Rendimiento con PDF

1. **Selección de Texto:** Asegúrate de que el PDF tenga texto seleccionable si es posible (aunque Claude usa visión, las capas de texto ayudan).
2. **Fragmentación (Chunking):** Para documentos que superan el límite de páginas, divide el PDF en fragmentos más pequeños o múltiples peticiones.
3. **Prompting:** Haz preguntas específicas. "Encuentra la tabla en la página 3 y extrae las cifras de ingresos."

## Próximos Pasos
- Aprende más sobre [Estrategias de Análisis de Documentos](08_analisis_documentos.md).
