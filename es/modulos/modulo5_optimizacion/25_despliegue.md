# 5.6 Estrategias de Despliegue

## Serverless (Lambda/Cloud Functions)
- **Pros:** Barato para tráfico bajo.
- **Contras:** "Arranques en frío" añaden latencia a la primera petición, y los tiempos límite de las funciones pueden ser más cortos que una generación larga. Usa streaming y establece tiempos de espera del cliente por debajo del límite de la función.

## Contenedores de Larga Duración (Fargate/K8s)
- **Pros:** Sin arranques en frío, mejor para conexiones de streaming (WebSockets).
- **Contras:** Cuestan dinero incluso cuando están inactivos.

## Despliegue en el Borde (Edge)
- **No posible** para Claude en sí (se ejecuta en servidores de Anthropic).
- **Posible** para el código del *cliente* (Vercel Edge Functions llamando a la API).

## Próximos Pasos
- [Integración con Plataforma en la Nube](26_integracion_nube.md).
