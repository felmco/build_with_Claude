# 2.3 Visión e Imágenes

Los modelos actuales de Claude son multimodales, lo que significa que pueden entender y analizar imágenes junto con el texto.

## Formatos Soportados
- **Formatos:** JPEG, PNG, GIF, WebP
- **Cantidad:** Hasta 600 imágenes por petición a la API (100 en Haiku 4.5, que tiene una ventana de contexto de 200K); 20 por mensaje en claude.ai.
- **Tamaño:** Máx. 10 MB por imagen (codificada en base64) en la API de Claude, máx. 8000x8000 px. Si una petición tiene más de 20 imágenes, cada imagen debe caber en 2000x2000 px. El límite total de la petición es 32 MB.
- **Redimensionado:** Las imágenes se procesan en parches de 28x28 px (un token visual cada uno). Las imágenes más grandes se reducen (borde largo de 1568 px en la mayoría de los modelos, 2576 px en Claude 4.7 y posteriores), así que redimensionarlas antes ahorra latencia y tokens.

## Cómo Enviar Imágenes

Puedes enviar imágenes como cadenas **Base64** (`"type": "base64"`), como **URLs** (`"type": "url"`) o como un **`file_id`** de la API de Archivos (`"type": "file"`, ver [API de Archivos](09_api_archivos.md)). Base64 funciona en todas partes, incluidos Amazon Bedrock y Google Cloud, que solo aceptan fuentes base64.

### Ejemplo Base64

```python
import anthropic
import base64
import httpx

# 1. Obtener datos de la imagen
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
response = httpx.get(image_url, follow_redirects=True, timeout=30)
response.raise_for_status()
image_data = base64.b64encode(response.content).decode("utf-8")

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message.content[0].text)
```

### Ejemplo con URL

```python
message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "url", "url": image_url}},
                {"type": "text", "text": "Describe this image."},
            ],
        }
    ],
)
```

Envía solo URLs de confianza, y ten en cuenta que la imagen debe ser accesible públicamente.

## Mejores Prácticas para Visión

1. **Calidad de Imagen:** Asegúrate de que el texto en las imágenes sea legible. Claude lee bien el texto pero lucha con texto muy borroso o pequeño.
2. **Colocación:** Pon las imágenes *antes* de las preguntas sobre ellas.
   - ✅ Imagen -> "¿Qué es esto?"
   - ❌ "¿Qué es esto?" -> Imagen
3. **Múltiples Imágenes:** Puedes incluir múltiples bloques de imagen en la lista `content` para pedir comparaciones. Etiqueta cada una con un breve bloque de texto ("Image 1:", "Image 2:") para poder referirte a ellas.

## Limitaciones

- **Personas:** Claude rechazará identificar (nombrar) personas reales en imágenes.
- **Médico:** No para uso diagnóstico (no está diseñado para escáneres complejos como TC o RM).
- **Espacial:** Ubicación aproximada de objetos, no coordenadas perfectas a nivel de píxel.
- **Conteo:** Los recuentos de muchos objetos pequeños son aproximados.
- **Generación:** Claude analiza imágenes; no puede generarlas ni editarlas.

## Próximos Pasos
- Aprende sobre [Soporte de PDF](07_soporte_pdf.md).
