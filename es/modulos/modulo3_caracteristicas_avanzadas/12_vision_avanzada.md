# 3.4 Técnicas Avanzadas de Visión

## 1. Múltiples Imágenes
Envía una serie de imágenes (fotogramas de un video, o páginas de un cómic) para contar una historia.

```python
content = []
for img_data in images:
    content.append({"type": "image", "source": {...}})
content.append({"type": "text", "text": "What is the sequence of events?"})
```

## 2. Transcribiendo Texto (OCR)
Claude es excelente en OCR (Reconocimiento Óptico de Caracteres), especialmente para notas escritas a mano.

**Prompt:**
> "Transcribe esta nota escrita a mano textualmente. Mantén los saltos de línea."

## 3. Extracción JSON desde UI
Muestra a Claude una captura de pantalla de un sitio web y pide una representación JSON de los campos.

**Prompt:**
> "Extrae el nombre del producto, precio y valoración de esta captura de pantalla en JSON."

## Próximos Pasos
- [Visión de Documentos](13_vision_documentos.md).
