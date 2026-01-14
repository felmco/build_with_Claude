# 3.4 Fundamentos de Visión

Cubrimos lo básico en el Módulo 2. Aquí profundizaremos más.

## Tamaño de Imágenes y Tokens

- **Borde Máximo:** 1568px (para procesamiento óptimo).
- **Redimensionamiento:** Si es más grande, la API lo redimensiona automáticamente, pero pagas latencia por la subida. Redimensiona en el *lado del cliente* para velocidad.
- **Coste:** ~1600 tokens máx para imágenes de alta resolución.

## Ejemplo: Redimensionamiento en el Lado del Cliente (Python)

```python
from PIL import Image
import io

def resize_image(image_path, max_size=1568):
    with Image.open(image_path) as img:
        ratio = min(max_size / img.width, max_size / img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return buffer.getvalue()
```

## Próximos Pasos
- [Técnicas Avanzadas de Visión](./12_vision_advanced.md).
