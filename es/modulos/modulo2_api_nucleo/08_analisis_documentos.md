# 2.3 Estrategias de Análisis de Documentos

Una vez que puedes enviar PDFs o imágenes, ¿cómo obtienes el mejor análisis?

## 1. Extracción
Claude destaca en la conversión de datos de documentos no estructurados a JSON estructurado.

**Prompt:**
> "Extrae el número de factura, la fecha y el importe total de este documento. Devuelve JSON."

Para una salida que deba cumplir siempre un esquema, usa salidas estructuradas (`output_config={"format": {"type": "json_schema", ...}}`, ver [Gestionando Conversaciones](03_conversaciones.md)).

## 2. Resumen
Para documentos largos, pide resúmenes por niveles.

**Prompt:**
> "Proporciona un resumen ejecutivo de 1 frase, seguido de una lista con viñetas de los 3 riesgos principales mencionados en este contrato."

## 3. Análisis Visual (Gráficos y Tablas)
Claude puede interpretar gráficos en PDFs/Imágenes.

**Técnica:**
- Aísla el gráfico si es posible (recorta la imagen).
- Pregunta específicamente: "Analiza la tendencia en el gráfico de barras de la página 5."

## 4. Comparaciones
Envía dos documentos (ej. Contrato V1 y Contrato V2) y pide una diferencia (diff).

```python
# doc_v1 / doc_v2: cadenas base64 de PDF (o usa fuentes {"type": "file", "file_id": ...})
messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "Version 1:"},
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": doc_v1}},
        {"type": "text", "text": "Version 2:"},
        {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": doc_v2}},
        {"type": "text", "text": "Highlight the changes in the liability clause."},
    ]}
]
```

## Manejo de Diseños Complejos
Los PDFs con múltiples columnas o tablas complejas pueden ser difíciles.
- **Consejo:** Pide a Claude que lea la tabla fila por fila, o sube `output_config.effort`, si lee mal una tabla.
- **Consejo:** Usa herramientas de extracción en modo `text` (Python `pypdf`) junto con la visión de Claude para verificación.

## Próximos Pasos
- Aprende sobre la [API de Archivos](09_api_archivos.md) para una gestión más fácil.
