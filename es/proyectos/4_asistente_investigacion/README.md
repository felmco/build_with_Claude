# 4 Asistente de Investigación

Una CLI de investigación multi-agente. Un agente **lead** divide tu pregunta en 3-5 subpreguntas, los agentes **worker** las investigan en paralelo con las herramientas de búsqueda web y de obtención web (web fetch) del lado del servidor de Anthropic, y un **synthesizer** escribe un informe en markdown con citas numeradas, una sección de Fuentes y una sección que señala las afirmaciones contradictorias o de baja confianza. El informe se guarda en `reports/<slug>.md`.

```
python main.py "How effective are heat pumps in cold climates?"
python main.py --offline-demo        # todo el pipeline con datos enlatados, sin clave ni red
```

> Nota: los prompts del código se mantienen en inglés para que el código y las pruebas sean idénticos a los de la versión en inglés. Puedes localizarlos a tu idioma si lo deseas.

## Arquitectura

```
question
   |
   v
[lead: claude-sonnet-5-5]  structured output (output_config.format JSON schema)
   |  3-5 sub-questions
   v
asyncio.gather + Semaphore(concurrency)
 +--------------------+ +--------------------+ +--------------------+
 | worker 1 (haiku)   | | worker 2           | | worker N           |
 | web_search/fetch   | | loop on pause_turn | | max_uses caps      |
 +---------+----------+ +---------+----------+ +---------+----------+
           \                      |                      /
            v                     v                     v
       Findings: text + sources (url,title) + warnings + status
                              |
                              v
           SourceRegistry (one number per distinct URL)
                              |
                              v
[synthesizer: claude-sonnet-5-5]  writes report citing [n], flags conflicts
                              |
                              v
finalize_report: renumber by first use, unknown [n] -> [unverified],
build Sources section in code  ->  reports/<slug>.md

Budget guard (tokens / est. cost / tool uses) is checked before every API call.
```

Archivos: `main.py` (CLI), `research/agents.py` (plan, worker, synthesizer), `research/tools.py` (versiones de herramientas, lectura de bloques de resultado), `research/budget.py` (uso + guarda + `PRICES`), `research/report.py` (citas, guardado), `research/pipeline.py` (orquestación), `research/fake.py` (`FakeClient` offline y constructores para pruebas).

## Configuración

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # añade requirements-dev.txt para pytest
cp .env.example .env                     # después pon tu clave en .env
```

## Ejecución

```
python main.py "What do we know about intermittent fasting and longevity?"
python main.py "Rust vs Go for CLI tools" --worker-model claude-sonnet-5-5 --max-cost 2
python main.py "EU AI Act obligations" --allowed-domains europa.eu eur-lex.europa.eu
python main.py "question" --dry-run      # muestra la configuración y las definiciones de herramientas, sin llamadas a la API
```

El progreso va a stderr (`--quiet` lo oculta); después stdout termina con la ruta del informe y una línea de uso:

```
[lead:claude-sonnet-5-5] planning sub-questions
  1. Background: ...
[worker 1/3] searching: ...
[worker 1/3] ok, 5 sources (1/3 done, ~$0.041 so far)
...
Report saved to reports/how-effective-are-heat-pumps-in-cold-climates.md
Usage: 12 API calls, 85,000 in / 9,000 out (+0 cache read, 0 cache write), 14 tool uses (9 searches); estimated cost ~$0.2100 [...] (estimate, check your Console)
```

El contenido de `--offline-demo` es ficticio (fuentes `example.org`). Existe para mostrar el flujo: la reanudación de un `pause_turn`, un bloque de error de herramienta de servidor, afirmaciones contradictorias y una cita falsa convertida en `[unverified]`.

## Opciones

| Flag | Por defecto | Significado |
|---|---|---|
| `--model` | `claude-sonnet-5-5` | lead y synthesizer |
| `--worker-model` | `claude-haiku-4-5` | workers |
| `--concurrency` | 3 | workers en paralelo (semáforo) |
| `--max-searches` / `--max-fetches` | 4 / 3 | `max_uses` por worker |
| `--allowed-domains` / `--blocked-domains` | ninguno | una u otra (la API rechaza ambas) |
| `--max-total-tokens` / `--max-cost` / `--max-tool-uses` | 400000 / 1.00 / 40 | presupuesto de la ejecución |
| `--out-dir` | `reports` | directorio de salida |

### Compromiso del modelo worker

Las herramientas web `_20260209` (filtrado dinámico: la API ejecuta código para recortar las páginas antes de que entren en el contexto) requieren modelos de la clase Sonnet 4.6+ / Opus 4.6+. Haiku 4.5 es más barato pero recibe las versiones básicas `web_search_20250305` / `web_fetch_20250910`, así que las páginas entran en el contexto sin filtrar y cuestan más tokens. `build_tools()` elige la versión automáticamente según el nombre del modelo. Si la calidad de las respuestas o el coste en tokens con Haiku te decepciona, prueba `--worker-model claude-sonnet-5-5`: cuesta 2x por token, pero filtra las páginas y razona mejor.

## Características de Claude demostradas

| Característica | Dónde | Lección |
|---|---|---|
| Salida estructurada con un esquema JSON (`output_config.format`) | `agents.plan` | [6.2 Salidas estructuradas y rechazos](../../modulos/modulo6_caracteristicas_plataforma/02_salidas_estructuradas_rechazos.md) |
| Herramientas de servidor: búsqueda y obtención web, `max_uses`, listas de dominios | `tools.build_tools` | [6.1 Herramientas de servidor](../../modulos/modulo6_caracteristicas_plataforma/01_herramientas_servidor.md) |
| Reanudación de `pause_turn`, errores devueltos con HTTP 200 | `agents.run_worker`, `tools.server_tool_errors` | 6.1 |
| Manejo de `stop_reason`: `refusal`, `max_tokens`, `pause_turn` | `agents.py` | 6.2 |
| Patrón multi-agente orquestador-worker | `pipeline.py` | [4.7 Multi-agente](../../modulos/modulo4_aplicaciones/07_multi_agente.md) |
| `AsyncAnthropic`, `asyncio.gather`, semáforo | `pipeline.py` | [5.12 Concurrencia asíncrona](../../modulos/modulo5_optimizacion/12_async_concurrencia.md) |
| Seguimiento de uso y estimación de costes | `budget.py` | [1.3 Precios](../../modulos/modulo1_fundamentos/03_precios_limites.md), [5.6 Optimización de tokens](../../modulos/modulo5_optimizacion/06_optimizacion_tokens.md) |
| Defensa contra inyección de prompts | prompts, `report.py` | [5.21 Seguridad](../../modulos/modulo5_optimizacion/21_seguridad.md) |
| Pruebas con un cliente falso | `tests/` | [4.20 Pruebas](../../modulos/modulo4_aplicaciones/20_pruebas.md) |

Las fuentes oficiales están en [REFERENCIAS.md](../../REFERENCIAS.md).

## Guarda de presupuesto

`Budget.check()` se ejecuta antes de cada llamada a la API y lanza `BudgetExceeded` cuando los tokens, el coste estimado o los usos de herramientas alcanzan el límite. Un worker que lo alcanza devuelve lo que tiene con estado `budget`; si el synthesizer no puede ejecutarse, se escribe un informe con los hallazgos en bruto sin llamar al modelo. Los límites son blandos: las peticiones que ya están en curso (hasta 3 workers) pueden sobrepasarlos, y el coste usa la tabla `PRICES` de `research/budget.py` (lecturas de caché al 10 %, escrituras a 1.25x, búsquedas a 0,01 $ cada una). Es una estimación, no tu factura.

## Notas de seguridad

- Las páginas web obtenidas no son confiables y pueden contener inyección de prompts. A los workers se les indica que traten el contenido solo como evidencia; el synthesizer recibe los hallazgos dentro de etiquetas `<findings>` como datos. Esto reduce el riesgo, no lo elimina.
- Los workers no tienen herramientas del lado del cliente (sin acceso a archivos ni a shell), lo que limita lo que puede hacer una inyección. No añadas esas herramientas sin volver a pensar esto. Web fetch solo puede abrir URL que ya hayan aparecido en la conversación; usa `--allowed-domains` en entornos sensibles.
- Los números de cita se validan en código: el modelo nunca escribe la sección de Fuentes, los números desconocidos pasan a `[unverified]` y solo las URL `http(s)` se convierten en enlaces.
- El nombre del archivo del informe es un slug `[a-z0-9-]`, así que una pregunta no puede escribir fuera de `--out-dir`.
- La clave de API se lee de `ANTHROPIC_API_KEY` y nunca se imprime. Mantén `.env` fuera de git.

## Pruebas

```
pip install -r requirements-dev.txt
pytest -q
```

31 pruebas offline cubren el parseo del plan y el uso del esquema, el bucle de `pause_turn` (forma de la reanudación, límite), las versiones de herramientas por modelo, los bloques de error de herramientas de servidor, rechazo / `max_tokens` / errores de la API, la guarda de presupuesto, la renumeración de citas, las URL inseguras, la seguridad del slug, la concurrencia con semáforo, los fallbacks y la demo offline de extremo a extremo.

## Límites

- No se ha ejecutado contra la API real en este repositorio (no había clave durante el desarrollo). Las formas de las peticiones se comprobaron contra el SDK `anthropic` instalado y la documentación del curso; espera tener que ajustar en la primera ejecución real. En particular, aquí no se ha verificado si Haiku 4.5 acepta la herramienta básica de fetch en tu organización y región.
- Las versiones de herramientas con filtrado dinámico `_20260209` se usan para Sonnet/Opus; existen versiones más nuevas, consulta la referencia de herramientas.
- Los workers se ejecutan sin streaming con `max_tokens=4096`; los turnos largos con herramientas de servidor pueden ser lentos.
- En `pause_turn` el worker reenvía todo el contenido del asistente acumulado hasta el momento. Si resulta que la API devuelve el contenido completo al reanudar, elimina la acumulación en `run_worker`.
- Las afirmaciones son tan buenas como las páginas recuperadas; el informe señala los conflictos pero no los verifica.

## Amplíalo

- Haz streaming del progreso por worker (`client.messages.stream`) para una salida de progreso más fina.
- Añade un agente crítico que vuelva a comprobar las afirmaciones de una sola fuente con una segunda búsqueda.
- Cachea los prompts de sistema del planner y del synthesizer ([caché de prompts](../../modulos/modulo3_caracteristicas_avanzadas/05_cache_prompt.md)).
- Usa la Batch API para investigaciones no urgentes a mitad de precio.
- Reintenta una vez los workers fallidos con un modelo más potente.
