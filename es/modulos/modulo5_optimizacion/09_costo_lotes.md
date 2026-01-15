# 5.2 Procesamiento por Lotes para Reducción de Costes

## La Regla del 50%
Cualquier cosa que no necesite ser respondida en <10 segundos debería ir a Lotes (Batch).

## Arquitectura
1. **Cola:** Acumula peticiones no urgentes en una tabla de DB.
2. **Trabajo Cron:** Cada 5 minutos, consulta la tabla.
3. **Enviar:** Si > 100 peticiones (o si la más antigua es > 1 hora), envía un lote.
4. **Recuperar:** Sondea resultados y actualiza la DB.

## Ejemplo de Ahorro de Costes
- **Escenario:** Procesando 1M documentos/mes con Sonnet.
- **Estándar:** $3 entrada + $15 salida / MTok.
- **Lote:** $1.50 entrada + $7.50 salida.
- **Ahorro:** Miles de dólares.

## Próximos Pasos
- Muévete a [Optimización de Latencia](10_latencia.md).
