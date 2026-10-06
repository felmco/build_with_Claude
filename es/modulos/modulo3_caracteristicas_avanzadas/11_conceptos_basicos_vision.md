# 3.4 Fundamentos de Visión

Cubrimos lo básico en el Módulo 2. Aquí profundizaremos más.

## Formatos y Límites Soportados

- **Formatos:** solo JPEG, PNG, GIF y WebP (los GIF animados usan el primer fotograma). Convierte antes TIFF, BMP, etc.
- **Tamaño:** hasta 10 MB por imagen (codificada en base64) en la API de Claude; 5 MB en Amazon Bedrock y Google Cloud.
- **Cantidad:** hasta 600 imágenes por petición a la API (100 para modelos con contexto de 200K, como Haiku 4.5), sujeto al límite de 32 MB por petición. Por encima de 20 imágenes por petición, cada imagen debe medir como máximo 2000 px por lado.
- **Dimensiones:** hasta 8000x8000 px por imagen.
- **Fuentes:** `base64`, `url`, o un `file_id` de la Files API (súbela una vez, reutilízala muchas veces).

## Tamaño de Imágenes y Tokens

Claude ve una imagen como parches de 28x28 píxeles, así que una imagen cuesta aproximadamente `ceil(ancho/28) x ceil(alto/28)` tokens.

| Nivel | Modelos | Borde largo máx. | Tokens máx. por imagen |
|-------|---------|------------------|------------------------|
| Alta resolución | Claude 4.7 y posteriores (Fable 5.1, Opus 5.5, Sonnet 5.5) | 2576 px | 4784 |
| Estándar | Otros (p. ej. Haiku 4.5) | 1568 px | 1568 |

- **Redimensionamiento:** Las imágenes más grandes se reducen automáticamente, así que pagas tiempo de subida y latencia por píxeles que se descartan. Redimensiona en el *lado del cliente* al límite del nivel, o menos si no necesitas el detalle (una imagen de 1000x1000 son unos 1300 tokens).
- **Orden:** Pon las imágenes antes de la pregunta de texto cuando puedas.
- **Control de costes:** Los modelos de alta resolución pueden usar unas 3 veces más tokens por imagen grande que los estándar. Reduce la resolución si no necesitas detalle fino.

## Ejemplo: Redimensionamiento en el Lado del Cliente (Python)

```python
import base64
import io

from PIL import Image

def prepare_image(image_path, max_size=1568):
    """Reduce una imagen y devuelve un JPEG en base64 listo para la API."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # JPEG no puede almacenar modos alfa/paleta
        ratio = min(max_size / img.width, max_size / img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

# Uso
# image_block = {
#     "type": "image",
#     "source": {"type": "base64", "media_type": "image/jpeg", "data": prepare_image("photo.png")},
# }
```

Una compresión JPEG fuerte puede dificultar la lectura de texto pequeño, así que mantén la calidad alta para documentos y capturas de pantalla.

## Próximos Pasos
- [Técnicas Avanzadas de Visión](12_vision_avanzada.md).
