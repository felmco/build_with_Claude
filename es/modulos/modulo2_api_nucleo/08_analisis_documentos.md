# 2.3 Estrategias de Análisis de Documentos

Una vez que puedes enviar PDFs o imágenes, ¿cómo obtienes el mejor análisis?

## 1. Extracción
Claude destaca en la conversión de datos de documentos no estructurados a JSON estructurado.

**Prompt:**
> "Extrae el número de factura, la fecha y el importe total de este documento. Devuelve JSON."

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
messages=[
    {"role": "user", "content": [
        {"type": "document", "source": {...data_v1...}}, # Doc 1
        {"type": "text", "text": "Here is Version 1."},
        {"type": "document", "source": {...data_v2...}}, # Doc 2
        {"type": "text", "text": "Here is Version 2. Highlight the changes in the liability clause."}
    ]}
]
```

## Manejo de Diseños Complejos
Los PDFs con múltiples columnas o tablas complejas pueden ser difíciles.
- **Consejo:** Pide a Claude que "Piense paso a paso sobre el diseño" si lee mal una tabla.
- **Consejo:** Usa herramientas de extracción en modo `text` (Python `pypdf`) junto con la visión de Claude para verificación.

## Próximos Pasos
- Aprende sobre la [API de Archivos](09_api_archivos.md) para una gestión más fácil.
