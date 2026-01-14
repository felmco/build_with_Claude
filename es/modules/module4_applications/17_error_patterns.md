# 4.5 Patrones de Error en Producción

En producción, debes manejar más que solo excepciones.

## 1. El Bucle de "Rechazo"
Claude rechaza una solicitud ("No puedo ayudar con eso").
- **Solución:** Ajusta el Prompt del Sistema. Detecta palabras clave de rechazo y recurre a un humano.

## 2. La Comprobación de "Alucinaciones"
- **Patrón:** Usa un segundo modelo más pequeño para verificar la salida del primer modelo.
- **Prompt:** "¿Contradice esta respuesta el contexto proporcionado?"

## 3. El Fallo de "Análisis de Salida"
- **Patrón:** Claude devuelve JSON inválido.
- **Solución:** Usa un bucle de reintento (máx 3 intentos) pasando el mensaje de error de vuelta a Claude. "Devolviste JSON inválido aquí: [Error]. Por favor arregla."

## Próximos Pasos
- [Estrategias de Limitación de Velocidad](./18_rate_limiting.md).
