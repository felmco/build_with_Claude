# 3.3 Casos de Uso de Lotes

¿Cuándo deberías usar la API por Lotes?

## Escenarios Ideales

1. **Categorización de Datos a Gran Escala**
   - Tienes 50,000 reseñas de clientes.
   - Necesitas análisis de sentimiento.
   - Sensibilidad temporal: Baja (puede esperar durante la noche).
   - Beneficio: Enorme ahorro de costes.

2. **Generación de Contenido**
   - Generar 1,000 artículos SEO.
   - Crear datos de entrenamiento sintéticos.

3. **Migración / Traducción**
   - Traducir un sitio de documentación completo.
   - Convertir código de Python 2 a 3.

## Cuándo NO usar Lotes

- Chatbots (necesitan tiempo real).
- Bucles de agentes (necesitan retroalimentación inmediata).
- Alertas críticas sensibles al tiempo.

## Próximos Pasos
- Aprende cómo [Monitorizar Trabajos por Lotes](10_monitoreo_lotes.md).
