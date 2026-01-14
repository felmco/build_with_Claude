# 5.4 Pruebas A/B de Prompts

En producción, puedes probar mejoras con tráfico real.

## Configuración
1. **Config:** Almacena prompts en una DB o sistema de feature flags.
2. **Enrutador:** Asigna 50% de tráfico al Prompt A, 50% al Prompt B.
3. **Rastreo:** Registra qué prompt se usó para cada ID de petición.

## Métrica de Éxito
¿Cómo sabes cuál es mejor?
- **Retroalimentación de Usuario:** Pulgar arriba/abajo.
- **Conversión:** ¿Copió el usuario el código? ¿Compró el artículo?
- **Retención:** ¿Volvió?

## Próximos Pasos
- [Métricas de Calidad](./17_quality_metrics.md).
