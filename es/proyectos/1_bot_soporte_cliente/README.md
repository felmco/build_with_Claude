# 1. Bot de soporte al cliente

Un chatbot de soporte por línea de comandos para una tienda ficticia ("Example Shop"), construido con el SDK oficial de Python `anthropic`. Responde en streaming, consulta una pequeña base de conocimiento local, abre tickets, escala a una persona, responde en el idioma del cliente y registra el uso y el costo de cada turno.

> **Nota:** el código es idéntico al del proyecto en inglés para que las pruebas sigan siendo válidas. Los prompts del sistema y los mensajes de la interfaz del bot están en inglés; puedes localizarlos (por ejemplo, en `support_bot/prompts.py`) si quieres una versión totalmente en español.

## Arquitectura

```
 you ──► main.py (REPL: /stats /reset /quit, input checks)
              │
              ▼
        SupportBot.ask()  ── sanitize_input (empty / >2000 chars rejected)
              │              trim_history  (cut only at real user messages)
              ▼
   ┌─► client.messages.stream(system[cache_control], tools[cache_control], messages)
   │        │  text_stream ──► printed live;  get_final_message() ──► usage + stop_reason
   │        ▼
   │   stop_reason?
   │    ├ end_turn / max_tokens ─► done (max_tokens: notice shown)
   │    ├ refusal ───────────────► roll the turn back, polite message
   │    └ tool_use ─► SupportTools.execute() for every tool_use block
   │                   • search_knowledge_base  (keyword score over data/kb.json, results in <kb_document> tags)
   │                   • create_ticket          (validated, appended to data/tickets.jsonl)
   │                   • escalate_to_human      (appended to data/escalations.jsonl)
   └──────────── ONE user message holding all tool_results (is_error=true on failures)
              │
              ▼
        AnalyticsLog ──► logs/analytics.jsonl (one row per turn) ──► /stats
```

Archivos: `main.py` (CLI), `support_bot/bot.py` (bucle), `tools.py`, `history.py`, `analytics.py`, `prompts.py`, `offline.py` (stub para dry-run), `tests/`.

## Configuración

```bash
pip install -r requirements.txt            # add requirements-dev.txt for pytest
cp .env.example .env                       # then put your key in ANTHROPIC_API_KEY
python main.py --help
```

Instala también `requirements-dev.txt` si quieres ejecutar pytest.

## Ejecución

```bash
python main.py                    # claude-sonnet-5-5
python main.py --model claude-haiku-4-5       # cheaper (do not combine with --effort)
python main.py --effort low       # less thinking, faster, cheaper for simple chat
python main.py --dry-run          # offline demo with a stub "client": no key, no network
```

Forma esperada de una sesión (el texto será distinto):

```
You: Quiero devolver unos zapatos, ¿cuánto tarda el reembolso?
Aria: Puedes devolverlos en 30 días ... el reembolso llega en 5-7 días laborables ...
You: /stats
All time: 3 turns, 0 errors | tokens in=... out=... cache_read=... (hit rate 62%) | latency avg=2.10s p95=3.4s | tools: search_knowledge_base=2 | est. cost $0.0123
```

`--dry-run` sustituye a Claude por `support_bot/offline.py`, que no es un LLM: busca en la base de conocimiento y cita el mejor artículo. Úsalo para explorar el REPL y las herramientas, no para juzgar la calidad de las respuestas.

## Características de Claude que se demuestran

| Característica | Dónde | Lección del curso |
|---|---|---|
| Streaming (`client.messages.stream`, `text_stream`, `get_final_message`) | `bot.py` | [2.4 Conceptos básicos de streaming](../../modulos/modulo2_api_nucleo/04_conceptos_basicos_streaming.md), [2.5 Streaming avanzado](../../modulos/modulo2_api_nucleo/05_streaming_avanzado.md) |
| Prompt de sistema, reglas de idioma, reglas contra inyección | `prompts.py` | [2.2 Prompts de sistema](../../modulos/modulo2_api_nucleo/02_prompts_sistema.md) |
| Historial de conversación y recorte | `history.py` | [2.3 Conversaciones](../../modulos/modulo2_api_nucleo/03_conversaciones.md) |
| Uso de herramientas, bucle de agente manual, resultados en paralelo en un solo mensaje, `is_error` | `bot.py`, `tools.py` | [3.1 Uso de herramientas](../../modulos/modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md), [3.2 Herramientas personalizadas](../../modulos/modulo3_caracteristicas_avanzadas/02_herramientas_personalizadas.md), [4.6 Bucles de agente](../../modulos/modulo4_aplicaciones/06_bucles_agente.md) |
| Caché de prompts (`cache_control` en la última herramienta y en el bloque de sistema) | `bot.py`, `tools.py` | [3.5 Caché de prompts](../../modulos/modulo3_caracteristicas_avanzadas/05_cache_prompt.md) |
| Manejo de rechazos y de `max_tokens` | `bot.py` | [6.2 Salidas estructuradas y rechazos](../../modulos/modulo6_caracteristicas_plataforma/02_salidas_estructuradas_rechazos.md) |
| Seguimiento de uso, estimación de costo, registro en JSONL | `analytics.py` | [1.3 Precios y límites](../../modulos/modulo1_fundamentos/03_precios_limites.md), [4.19 Registro y monitoreo](../../modulos/modulo4_aplicaciones/19_registro_monitoreo.md) |
| Higiene frente a inyección de prompts, límites de entrada | `bot.py`, `tools.py` | [5.21 Seguridad](../../modulos/modulo5_optimizacion/21_seguridad.md) |
| Pruebas con un cliente falso | `tests/` | [4.20 Pruebas](../../modulos/modulo4_aplicaciones/20_pruebas.md) |

Documentación oficial: consulta [REFERENCIAS.md](../../REFERENCIAS.md) (uso de herramientas, caché de prompts, streaming, errores).

## Configuración de opciones

| Opción | Valor por defecto | Significado |
|---|---|---|
| `--model` | `claude-sonnet-5-5` | Cualquier ID de modelo. Las estimaciones de costo usan la tabla `PRICES` de `analytics.py` (los modelos desconocidos usan los precios de Sonnet). |
| `--max-tokens` | 1024 | Límite de salida por llamada a la API. |
| `--effort` | sin definir | `low`/`medium`/`high`, enviado como `output_config.effort`. No es compatible con Haiku 4.5. |
| `--kb`, `--tickets`, `--log` | `data/kb.json`, `data/tickets.jsonl`, `logs/analytics.jsonl` | Ubicación de los archivos. |
| `--max-history` | 40 | Máximo de mensajes conservados (además, un tope de 40k caracteres en `history.py`). |
| `--dry-run` | desactivado | Cliente stub sin conexión. |

Entorno: `ANTHROPIC_API_KEY` (se lee del entorno o de `.env`; nunca se imprime).
No se usan parámetros de muestreo (`temperature`, etc.), prefill del asistente ni `budget_tokens`; los modelos actuales los rechazan.

## Notas de seguridad

- **Texto no confiable de la base de conocimiento**: los artículos se devuelven dentro de las etiquetas `<knowledge_base_results>/<kb_document>`, se escapan `<` y `>` para que el texto no pueda cerrar las etiquetas, y el prompt de sistema indica tratar ese contenido como datos. Esto reduce el riesgo de inyección, pero no lo elimina.
- **Los argumentos de las herramientas no son confiables**: se validan (enums, formato de correo, límites de longitud); una entrada incorrecta devuelve `is_error: true` para que Claude pueda corregirse. Nada se ejecuta como código ni como shell.
- **Límites de entrada**: se eliminan los caracteres de control y se rechaza lo vacío o de más de 2000 caracteres (nunca se trunca en silencio).
- Los tickets y el registro de analítica son archivos de texto plano que contienen texto y correos de clientes; aquí están en el `.gitignore`. Aplica tu propia política de retención y privacidad antes de un uso real.
- El bot no puede emitir reembolsos ni verificar identidades; solo describe políticas y abre tickets.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest -q          # 26 tests, offline, fake client in tests/conftest.py
```

Cubren el bucle de streaming y herramientas, los resultados de herramientas en un solo mensaje, los parámetros de caché, el rechazo, `max_tokens`, la reversión ante errores de la API, las invariantes del recorte de historial, la puntuación de la base de conocimiento y el escape de etiquetas, la validación de tickets, los límites de entrada y el cálculo de costos. Las pruebas importan `httpx2` (la biblioteca HTTP que usa `anthropic` 1.x) para construir un error de límite de velocidad.

## Límites y advertencias honestas

- No se ejecutó contra la API real en el entorno de construcción de este repositorio: la forma de las solicitudes se comprobó solo contra las firmas del SDK instalado y la documentación oficial. Haz una prueba de humo con una clave real.
- El caché solo se activa por encima de un prefijo mínimo que depende del modelo (aproximadamente 1-4k tokens). Este prompt de sistema pequeño más tres herramientas puede quedar por debajo, así que `cache_read` puede seguir en 0 hasta que amplíes el prompt o las instrucciones de la base de conocimiento. `/stats` muestra si hay aciertos.
- La puntuación por palabras clave es básica (sin stemming, sin sinónimos, base de conocimiento solo en inglés; Claude traduce las consultas). Sustitúyela por embeddings (de un proveedor externo, ya que Anthropic no tiene un endpoint de embeddings) para una base de conocimiento real.
- El recorte del historial descarta turnos antiguos completos sin resumirlos, así que el bot olvida el contexto más antiguo. Además cambia el prefijo de mensajes, por lo que tras un recorte solo sobrevive el caché del sistema y de las herramientas.
- Los bloques de pensamiento (si el modelo emite alguno) se almacenan y se reenvían sin cambios dentro de una conversación.
- Las cifras de costo son estimaciones a partir de una tabla de precios fija y pueden desviarse de la página de precios.
- Un solo usuario, un solo proceso, sin persistencia de conversaciones, sin autenticación.

## Amplíalo

- Cambia la búsqueda por palabras clave por embeddings, o carga la base de conocimiento desde archivos markdown.
- Añade `get_order_status` contra un sistema real de pedidos (mantenlo de solo lectura y comprueba la identidad de quien consulta).
- Resume los turnos recortados, o usa compactación del lado del servidor para chats largos.
- Ejecuta un paso de triaje con Haiku 4.5 para enrutar a bajo costo las preguntas sencillas.
- Envuelve `SupportBot` en un manejador web o de una plataforma de chat; mantén un `SupportBot` por cliente.
