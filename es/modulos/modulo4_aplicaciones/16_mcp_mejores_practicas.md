# 4.4 Mejores Prácticas de MCP

1. **Seguridad:** Los servidores MCP ejecutan código local. No conectes servidores no confiables.
2. **Recurso vs Herramienta:**
   - Usa **Recursos** para datos pasivos (logs, contenido de archivo).
   - Usa **Herramientas** para acciones (consultas, llamadas API).
3. **Manejo de Errores:** Devuelve errores significativos para que el modelo pueda reintentar (los resultados de herramientas MCP admiten una bandera `isError`).
4. **Stdio vs Streamable HTTP:**
   - **Stdio:** Mejor para apps de escritorio locales.
   - **Streamable HTTP:** Mejor para servidores remotos. Reemplaza al transporte anterior HTTP+SSE, que está obsoleto.

## Próximos Pasos
- Muévete a [Patrones de Producción](17_patrones_error.md).
