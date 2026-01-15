# 1.1 Precios y Límites del Modelo

Entender la estructura de costes y los límites de velocidad es crucial para construir aplicaciones sostenibles con Claude.

## Visión General de Precios (a partir de 2026)

El precio se basa en **tokens**.
- **Tokens de Entrada**: Texto que envías a Claude (prompts, documentos).
- **Tokens de Salida**: Texto que Claude genera.

| Modelo | Coste de Entrada (por MTok) | Coste de Salida (por MTok) |
|-------|------------------------|-------------------------|
| **Claude Haiku 3.5** | $0.80 | $4.00 |
| **Claude Haiku 4.5** | $1.00 | $5.00 |
| **Claude Sonnet 4.5** | $3.00 | $15.00 |
| **Claude Opus 4.5** | $5.00 | $25.00 |

*MTok = Millón de Tokens*

### Precios de Caché de Prompts
El almacenamiento en caché de prompts te permite almacenar grandes contextos (como libros, bases de código) para reducir los costes de entrada.

- **Escritura en Caché**: Coste más alto (procesamiento inicial)
- **Lectura de Caché**: Coste significativamente más bajo (~10% de la entrada estándar)

| Modelo | Escritura en Caché (5m) | Escritura en Caché (1h) | Lectura de Caché |
|-------|------------------|------------------|------------|
| **Sonnet 4.5** | $3.75 / MTok | $6.00 / MTok | $0.30 / MTok |
| **Haiku 4.5** | $1.25 / MTok | $2.00 / MTok | $0.10 / MTok |

## Límites de Velocidad

Los límites de velocidad determinan cuántas peticiones puedes hacer por minuto (RPM) y cuántos tokens puedes consumir por minuto (TPM). Los límites varían por **Nivel (Tier)**.

### Niveles de Uso

| Nivel | Descripción | Límites Típicos (Sonnet) |
|------|-------------|-------------------------|
| **Gratis / Nivel 1** | Cuentas nuevas | RPM bajo (ej., 5-50) |
| **Nivel 2** | Uso activo | RPM moderado (ej., 1000) |
| **Nivel 3** | Alto volumen | RPM alto (ej., 2000+) |
| **Nivel 4** | Enterprise | Personalizado / Límites máximos |

*Nota: Consulta tus límites específicos en la [Consola de Anthropic](https://console.anthropic.com/settings/limits).*

## Gestionando Costes

### 1. Estima el Conteo de Tokens
Usa la herramienta tokenizer o la API para estimar el uso.
```python
# Aproximado: 1000 tokens ≈ 750 palabras
word_count = len(text.split())
estimated_tokens = word_count * 1.33
cost = (estimated_tokens / 1_000_000) * 3.00  # Para Entrada Sonnet
```

### 2. Establece `max_tokens`
Siempre establece un límite de `max_tokens` en tus llamadas a la API para prevenir salidas grandes inesperadas (y costes) si el modelo entra en bucle o genera demasiado texto.

### 3. Usa Caché para Contextos Largos
Si envías el mismo documento largo múltiples veces, usa Caché de Prompts para ahorrar hasta un 90% en costes de entrada.

## Próximos Pasos
- Configura tu entorno en [Instalando Python y Dependencias](04_configuracion_python.md).
