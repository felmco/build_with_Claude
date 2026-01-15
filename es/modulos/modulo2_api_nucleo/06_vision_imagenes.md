# 2.3 Visión e Imágenes

Los modelos de Claude (familia Claude 3 y posteriores) son multimodales, lo que significa que pueden entender y analizar imágenes junto con el texto.

## Formatos Soportados
- **Formatos:** JPEG, PNG, GIF, WebP
- **Límite:** Hasta 100 imágenes por petición (API), 20 (Claude.ai).
- **Tamaño:** Recomendado < 1.15 MP para velocidad. Max 8000x8000px.

## Cómo Enviar Imágenes

Puedes enviar imágenes como cadenas codificadas en **Base64** o vía **URLs** (dependiendo de la versión del SDK/soporte de características). La forma más robusta en la API es Base64.

### Ejemplo Base64

```python
import anthropic
import base64
import httpx

# 1. Obtener datos de la imagen
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image_media_type = "image/jpeg"
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
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

## Mejores Prácticas para Visión

1. **Calidad de Imagen:** Asegúrate de que el texto en las imágenes sea legible. Claude lee bien el texto pero lucha con texto muy borroso o pequeño.
2. **Colocación:** Pon las imágenes *antes* de las preguntas sobre ellas.
   - ✅ Imagen -> "¿Qué es esto?"
   - ❌ "¿Qué es esto?" -> Imagen
3. **Múltiples Imágenes:** Puedes incluir múltiples bloques de imagen en la lista `content` para pedir comparaciones.

## Limitaciones

- **Personas:** Claude rechazará identificar (nombrar) personas reales en imágenes.
- **Médico:** No para uso diagnóstico.
- **Espacial:** Ubicación aproximada de objetos, no coordenadas perfectas a nivel de píxel.

## Próximos Pasos
- Aprende sobre [Soporte de PDF](07_soporte_pdf.md).
