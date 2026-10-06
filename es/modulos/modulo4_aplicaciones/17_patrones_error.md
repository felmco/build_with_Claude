# 4.5 Patrones de Error en Producción

En producción, debes manejar más que solo excepciones.

## 1. El Bucle de "Rechazo"
Claude rechaza una solicitud ("No puedo ayudar con eso").
- **Detectar:** Comprueba `response.stop_reason == "refusal"` antes de leer `response.content`; `response.stop_details` explica el rechazo. No te apoyes en la coincidencia de palabras clave.
- **Solución:** Ajusta el Prompt del Sistema o recurre a un humano.

## 2. La Comprobación de "Alucinaciones"
- **Patrón:** Usa un segundo modelo más pequeño para verificar la salida del primer modelo.
- **Prompt:** "¿Contradice esta respuesta el contexto proporcionado?"

## 3. El Fallo de "Análisis de Salida"
- **Patrón:** Claude devuelve JSON inválido.
- **Mejor:** Usa salidas estructuradas (`output_config={"format": {...}}`, o `client.messages.parse`) para que la respuesta cumpla tu esquema JSON.
- **Alternativa:** Usa un bucle de reintento (máx 3 intentos) pasando el mensaje de error de vuelta a Claude. "Devolviste JSON inválido aquí: [Error]. Por favor arregla."

## 4. Errores de la API
Captura `anthropic.RateLimitError`, `anthropic.APIConnectionError` y `anthropic.APIStatusError` (primero la más específica). El SDK ya reintenta los errores transitorios (`max_retries=2` por defecto), así que añade tus propios reintentos solo por encima de eso.

## Próximos Pasos
- [Estrategias de Limitación de Velocidad](18_limite_velocidad.md).
