# 2.4 Visión General de la API de Archivos

La **API de Archivos** (disponible de forma general; no necesita cabecera beta) te permite subir archivos una vez y reutilizarlos a través de múltiples peticiones de mensajes. Esto ahorra ancho de banda y simplifica el código para activos repetidos.

## Modelos Soportados
- **Imágenes:** Todos los modelos actuales de Claude (bloques `image` con una fuente `file`).
- **PDFs y texto plano:** Todos los modelos actuales de Claude (bloques `document` con una fuente `file`).
- **CSV y otros archivos de datos:** Se usan con la herramienta de ejecución de código; para texto plano en un mensaje normal, un bloque de texto suele ser más sencillo.
- **Plataformas:** Disponible en la API de Claude; no en Amazon Bedrock ni Google Vertex AI (usa base64 allí).

## Flujo de Uso

1. **Subir** un archivo al almacenamiento de Anthropic.
2. **Recibir** un `file_id`.
3. **Referenciar** el `file_id` en tus mensajes.

## Beneficios
- **Eficiencia:** No re-subir cadenas Base64 en cada llamada.
- **Coste:** Sin sobrecarga de subida de red repetida (los costes de tokens aún aplican para el procesamiento).
- **Escala:** Gestión de activos más fácil.

## Límites y Facturación
- Tamaño máximo de archivo: 500 MB; almacenamiento total: 100 GB por organización.
- Los archivos persisten hasta que los elimines, así que borra los que ya no necesites.
- Las operaciones de subida, listado y eliminación son gratuitas. El contenido de un archivo usado en un mensaje se factura como tokens de entrada, igual que cualquier otro contenido, y la petición sigue contando para los límites de velocidad.
- Solo puedes descargar archivos creados por herramientas (como la ejecución de código), no los archivos que subiste.

## Próximos Pasos
- Mira el código para [Gestión de Archivos](10_gestion_archivos.md).
