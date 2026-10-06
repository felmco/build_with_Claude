# 3.4 Técnicas Avanzadas de Visión

## 1. Múltiples Imágenes
Envía una serie de imágenes (fotogramas de un video, o páginas de un cómic) para contar una historia.

```python
content = []
for i, img_data in enumerate(images, 1):  # images: lista de cadenas base64
    content.append({"type": "text", "text": f"Image {i}:"})  # etiqueta cada imagen
    content.append({
        "type": "image",
        "source": {"type": "base64", "media_type": "image/jpeg", "data": img_data},
    })
content.append({"type": "text", "text": "What is the sequence of events?"})

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": content}],
)
```

Claude conserva el acceso a las imágenes de turnos anteriores, pero cada petición las reenvía. Para muchas imágenes o conversaciones largas, súbelas una vez con la Files API (`client.files.upload(...)`) y referéncialas con `{"type": "file", "file_id": ...}` como fuente de la imagen.

## 2. Transcribiendo Texto (OCR)
Claude es bueno en OCR (Reconocimiento Óptico de Caracteres), incluidas muchas notas escritas a mano. Revisa las transcripciones importantes, ya que el texto pequeño o de baja calidad puede leerse mal.

**Prompt:**
> "Transcribe esta nota escrita a mano textualmente. Mantén los saltos de línea."

## 3. Extracción JSON desde UI
Muestra a Claude una captura de pantalla de un sitio web y pide una representación JSON de los campos.

**Prompt:**
> "Extrae el nombre del producto, precio y valoración de esta captura de pantalla en JSON."

## Limitaciones
- Claude no puede identificar personas por su rostro, y no puede generar ni editar imágenes.
- Los conteos, posiciones espaciales y cuadros delimitadores son aproximados. Verifícalos en trabajos de alto riesgo.
- Las imágenes muy pequeñas (menos de unos 200 px), rotadas o borrosas son más propensas a errores.

## Próximos Pasos
- [Visión de Documentos](13_vision_documentos.md).
