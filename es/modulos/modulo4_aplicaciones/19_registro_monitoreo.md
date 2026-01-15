# 4.5 Logging y Monitorización

## ¿Qué Registrar?
1. **Entradas/Salidas:** El prompt y respuesta completos (Ten cuidado con PII/Privacidad).
2. **Metadatos:** ID de Modelo, Latencia, Uso de Tokens, Coste.
3. **Retroalimentación de Usuario:** Pulgar arriba/abajo.

## Herramientas
- **LangSmith:** especializado para trazas de LLM.
- **Arize / Phoenix:** observabilidad de LLM.
- **Estándar:** Datadog, Prometheus.

## Alertas
- Alertar en **Tasa de Error > 1%**.
- Alertar en **Coste > Presupuesto**.
- Alertar en **Latencia > 5s**.

## Próximos Pasos
- [Pruebas](20_pruebas.md).
