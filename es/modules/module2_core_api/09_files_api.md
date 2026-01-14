# 2.4 Visión General de la API de Archivos

La **API de Archivos** (beta) te permite subir archivos una vez y reutilizarlos a través de múltiples peticiones de mensajes. Esto ahorra ancho de banda y simplifica el código para activos repetidos.

## Modelos Soportados
- **Imágenes:** Todos los modelos Claude 3+.
- **PDFs:** Todos los modelos Claude 3.5+.
- **CSV/Texto:** Soportado para herramientas específicas (Ejecución de Código), generalmente usa bloques de texto para estos en mensajes estándar.

## Flujo de Uso

1. **Subir** un archivo al almacenamiento de Anthropic.
2. **Recibir** un `file_id`.
3. **Referenciar** el `file_id` en tus mensajes.

## Beneficios
- **Eficiencia:** No re-subir cadenas Base64 en cada llamada.
- **Coste:** Sin sobrecarga de subida de red repetida (los costes de tokens aún aplican para el procesamiento).
- **Escala:** Gestión de activos más fácil.

## Nota Importante
Los archivos subidos vía la API **no** son persistentes para siempre por defecto en todos los contextos (aplican políticas de ciclo de vida), y los límites de uso de tokens estándar aún aplican cuando el contenido del archivo es procesado por el modelo.

## Próximos Pasos
- Mira el código para [Gestión de Archivos](./10_file_management.md).
