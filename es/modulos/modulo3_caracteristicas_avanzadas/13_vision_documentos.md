# 3.4 Visión de Documentos

Esto es distinto de la característica "Soporte de PDF". Esto se refiere a convertir *páginas* de documentos a imágenes tú mismo para un control de grano fino.

## ¿Por qué convertir a imágenes?
- **Anotaciones:** Puedes dibujar cajas rojas en la imagen para resaltar áreas antes de enviar a Claude.
- **Recortes específicos:** Envía solo un gráfico específico.
- **Formatos heredados:** TIFF, BMP, etc. La API solo acepta JPEG, PNG, GIF y WebP, así que convierte antes los demás formatos.

## Estrategia: Q&A Visual
1. Convierte página PDF a PNG.
2. Envía a Claude.
3. Mantén la página dentro de los límites de imagen de tu modelo (ver [Fundamentos de Visión](11_conceptos_basicos_vision.md)); el texto debe seguir siendo legible tras el redimensionamiento.
4. Pregunta: "¿Hay una firma en la esquina inferior derecha?"

Para PDFs simples, también puedes enviar el archivo directamente como un bloque de contenido `document` (base64, URL o `file_id` de la Files API) y omitir la conversión.

## Próximos Pasos
- Aprende sobre [Pensamiento Extendido](14_pensamiento_extendido.md).
