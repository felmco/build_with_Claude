# 1.1 Precios y Límites del Modelo

Entender la estructura de costes y los límites de velocidad es crucial para construir aplicaciones sostenibles con Claude.

## Visión General de Precios (octubre de 2026)

El precio se basa en **tokens**.
- **Tokens de Entrada**: Texto que envías a Claude (prompts, documentos).
- **Tokens de Salida**: Texto que Claude genera.

| Modelo | Coste de Entrada (por MTok) | Coste de Salida (por MTok) |
|-------|------------------------|-------------------------|
| **Claude Haiku 4.5** | $1.00 | $5.00 |
| **Claude Sonnet 5.5** | $2.00 | $10.00 |
| **Claude Opus 5.5** | $4.00 | $20.00 |
| **Claude Fable 5.1** | $10.00 | $50.00 |

*MTok = Millón de Tokens. Confirma siempre en la [página oficial de precios](https://platform.claude.com/docs/en/about-claude/pricing); los precios cambian.*

- **Batch API**: 50% de descuento en entrada y salida para trabajo asíncrono.
- Los **tokens de pensamiento** se facturan como tokens de salida.

### Precios de Caché de Prompts
El almacenamiento en caché de prompts te permite almacenar grandes contextos (como libros, bases de código) para reducir los costes de entrada.

- **Escritura en Caché**: 1.25x la entrada base (5 minutos) o 2x (1 hora)
- **Lectura de Caché**: una fracción pequeña del precio de entrada (10% en la mayoría; 5% en Opus 5.5; 2.5% en Fable 5.1)

| Modelo | Escritura en Caché (5m) | Escritura en Caché (1h) | Lectura de Caché |
|-------|------------------|------------------|------------|
| **Haiku 4.5** | $1.25 / MTok | $2.00 / MTok | $0.10 / MTok |
| **Sonnet 5.5** | $2.50 / MTok | $4.00 / MTok | $0.20 / MTok |
| **Opus 5.5** | $5.00 / MTok | $8.00 / MTok | $0.20 / MTok |
| **Fable 5.1** | $12.50 / MTok | $20.00 / MTok | $0.25 / MTok |

## Límites de Velocidad

Los límites de velocidad determinan cuántas peticiones puedes hacer por minuto (RPM) y cuántos tokens puedes consumir por minuto (TPM). Los límites varían por **Nivel (Tier)**.

### Niveles de Uso

| Nivel | Descripción | Límites Típicos (Sonnet) |
|------|-------------|-------------------------|
| **Gratis / Nivel 1** | Cuentas nuevas | RPM bajo (ej., 5-50) |
| **Nivel 2** | Uso activo | RPM moderado (ej., 1000) |
| **Nivel 3** | Alto volumen | RPM alto (ej., 2000+) |
| **Nivel 4** | Enterprise | Personalizado / Límites máximos |

*Nota: Consulta tus límites específicos en la [Consola de Claude](https://platform.claude.com/settings/limits) y la [documentación de límites](https://platform.claude.com/docs/en/api/rate-limits).*

## Gestionando Costes

### 1. Estima el Conteo de Tokens
Usa la API de conteo de tokens (`client.messages.count_tokens`) para medir el uso. Los modelos actuales usan un tokenizador más nuevo que genera más tokens por palabra, así que recalcula tu línea base al migrar.
```python
# Aproximado: 1000 tokens ≈ 750 palabras
word_count = len(text.split())
estimated_tokens = word_count * 1.33
cost = (estimated_tokens / 1_000_000) * 2.00  # Precio de entrada de Sonnet 5.5

# Mejor: cuenta con exactitud usando la API (sin tiktoken)
# n = client.messages.count_tokens(model="claude-sonnet-5-5", messages=[...]).input_tokens
```

### 2. Establece `max_tokens`
Siempre establece un límite de `max_tokens` en tus llamadas a la API para prevenir salidas grandes inesperadas (y costes) si el modelo entra en bucle o genera demasiado texto.

### 3. Usa Caché para Contextos Largos
Si envías el mismo documento largo múltiples veces, usa Caché de Prompts para ahorrar un 90% o más en costes de entrada.

## Próximos Pasos
- Configura tu entorno en [Instalando Python y Dependencias](04_configuracion_python.md).
