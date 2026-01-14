# 4.4 Mejores Prácticas de MCP

1. **Seguridad:** Los servidores MCP ejecutan código local. No conectes servidores no confiables.
2. **Recurso vs Herramienta:**
   - Usa **Recursos** para datos pasivos (logs, contenido de archivo).
   - Usa **Herramientas** para acciones (consultas, llamadas API).
3. **Manejo de Errores:** Devuelve errores significativos para que el modelo pueda reintentar.
4. **Stdio vs SSE:**
   - **Stdio:** Mejor para apps de escritorio locales.
   - **SSE (Eventos Enviados por el Servidor):** Mejor para servidores HTTP remotos.

## Próximos Pasos
- Muévete a [Patrones de Producción](./17_error_patterns.md).
