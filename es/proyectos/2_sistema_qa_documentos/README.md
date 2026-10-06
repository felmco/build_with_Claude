# Proyecto 2: Preguntas y respuestas sobre documentos (RAG) con citas

Una aplicación RAG de línea de comandos. Ingiere tus archivos `.txt`, `.md` y (opcionalmente) `.pdf`, los divide en fragmentos con solapamiento, los guarda en un índice JSON, recupera los mejores fragmentos para una pregunta y pide a Claude que responda **solo a partir de esos fragmentos**, con citas numeradas que apuntan al pasaje exacto.

> **Nota:** el código es idéntico al del proyecto en inglés para que las pruebas sigan siendo válidas. El prompt del sistema y los mensajes de la interfaz están en inglés; puedes localizarlos (por ejemplo, `SYSTEM_PROMPT` en `docqa/qa.py`) si quieres una versión totalmente en español.

## Arquitectura

```
 ingest                                   ask / chat
 ------                                   ----------
 files (txt/md/pdf)                       question
   |  docqa/ingest.py                       |
   v                                        v
 chunks (500 chars, 100 overlap)          retriever  <-- BM25 (default, pure Python)
   |  docqa/chunking.py                       |           or Voyage embeddings (optional)
   v                                          v  top-k chunks   docqa/retrieval.py
 index.json  ---- load ------------------>  document blocks {citations: enabled}
   docqa/index.py                             |  (+ cache_control on the last one)
   (+ optional Voyage vectors)                v   docqa/qa.py
                                          Claude (Messages API)
                                              |
                                              v
                                    answer text + [1][2] markers
                                    Sources: title, location, cited_text
```

Si la recuperación no encuentra nada, la aplicación responde "no está en los documentos" de forma local y no hace ninguna llamada a la API.

## Configuración

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then put your ANTHROPIC_API_KEY in .env
pip install pypdf               # optional: PDF ingestion
pip install voyageai            # optional: embeddings retriever
```

Pon tu `ANTHROPIC_API_KEY` en `.env`. `pypdf` (ingesta de PDF) y `voyageai` (recuperador con embeddings) son opcionales.

## Ejecútalo

```bash
python main.py ingest data/                       # builds index.json
python main.py search "how long is the warranty"  # offline: shows retrieved chunks
python main.py ask "How long do I have to return an item?"
python main.py ask "Do you ship to Brazil?" --dry-run   # retrieval only, no API call
python main.py chat                               # interactive; follow-ups reuse cached docs
```

Forma esperada de la salida de `ask` (el texto variará):

```
Items can be returned within 30 days of delivery for a full refund.[1]

Sources:
  [1] refund_policy.md [chars 0-474]  (chars 66-170)
      "Customers may return most items within 30 days of delivery for a full refund..."

usage: 1 request(s), in=1234 out=67 cache_read=0 cache_write=0 | ~$0.0031 (estimate)
```

Una pregunta que los documentos no pueden responder ("What is the CEO's salary?") produce: `The provided documents do not contain the answer to this question.`

Opciones útiles: `-k/--top-k`, `--model`, `--max-tokens`, `--no-cache`, `--dry-run`, `--retriever bm25|voyage|auto` y, para `ingest`: `--chunk-size`, `--overlap`, `--embed`. Ejecuta `python main.py <command> --help`.

## Características de Claude que se demuestran

| Característica | Dónde | Lección del curso |
|---|---|---|
| Bloques de contenido de documento (`source.type: "text"`) | `docqa/qa.py` `document_block` | [2.7 Soporte de PDF](../../modulos/modulo2_api_nucleo/07_soporte_pdf.md), [2.8 Análisis de documentos](../../modulos/modulo2_api_nucleo/08_analisis_documentos.md) |
| Citas (`citations: {"enabled": true}`; `cited_text`, `document_index`, ubicaciones por carácter) | `document_block`, `build_answer` | [2.8](../../modulos/modulo2_api_nucleo/08_analisis_documentos.md), [Documentación de la plataforma: citas](https://platform.claude.com/docs/en/build-with-claude/citations) |
| Caché de prompts (`cache_control` en el prefijo de documentos, seguimientos en `chat`) | `QASession.build_messages` | [3.5 Caché de prompts](../../modulos/modulo3_caracteristicas_avanzadas/05_cache_prompt.md) |
| Prompt de sistema que fuerza respuestas fundamentadas y "no está en los documentos" | `SYSTEM_PROMPT` | [2.2 Prompts de sistema](../../modulos/modulo2_api_nucleo/02_prompts_sistema.md) |
| RAG: dividir, indexar, recuperar, generar | todo `docqa/` | [4.9 Fundamentos de RAG](../../modulos/modulo4_aplicaciones/09_fundamentos_rag.md), [4.11 Embeddings](../../modulos/modulo4_aplicaciones/11_embeddings.md), [4.2 Sistemas de preguntas y respuestas](../../modulos/modulo4_aplicaciones/02_sistemas_qa.md) |
| Seguimiento de uso y costo, manejo de stop-reason (`refusal`, `max_tokens`, `pause_turn`) | `docqa/usage.py`, `build_answer` | [1.3 Precios y límites](../../modulos/modulo1_fundamentos/03_precios_limites.md) |
| Pruebas con un cliente falso | `tests/` | [4.20 Pruebas](../../modulos/modulo4_aplicaciones/20_pruebas.md) |

Todas las fuentes aparecen en [REFERENCIAS.md](../../REFERENCIAS.md).

## Recuperación: BM25 por defecto, Voyage opcional

**Anthropic no tiene una API de embeddings.** Claude no produce embeddings. Por eso el recuperador por defecto es BM25, un algoritmo de ranking por palabras clave implementado en unas 40 líneas de Python puro (`BM25Retriever`): sin servicios, sin claves. Su debilidad es la discrepancia de vocabulario ("coche" no coincidirá con "automóvil").

Para búsqueda semántica, la documentación de Anthropic apunta a Voyage AI, un proveedor aparte con su propia clave:

```bash
export VOYAGE_API_KEY=...        # or in .env
pip install voyageai
python main.py ingest data/ --embed          # stores voyage-3.5 vectors in index.json
python main.py ask "..." --retriever voyage  # or --retriever auto (falls back to BM25)
```

Las llamadas de embeddings envían el texto de tus fragmentos a Voyage AI. Los vectores se guardan como listas JSON y se comparan con similitud del coseno en Python puro, lo cual solo es adecuado para corpus pequeños.

## Cómo funcionan aquí las citas

Cada fragmento recuperado se convierte en su propio bloque `document` con el título `file [location]`. Los bloques de texto de Claude regresan con una lista `citations`; `document_index` indica qué bloque se citó y `start_char_index`/`end_char_index` son desplazamientos dentro de ese fragmento. La aplicación suma el desplazamiento inicial del fragmento para que la ubicación impresa sea un rango de caracteres en el archivo original (o, en los PDF, en la página; también se muestra el número de página). La misma cita se numera una sola vez, sin importar cuántas veces se cite.

Reglas que conviene recordar: las citas deben estar habilitadas en todos los documentos o en ninguno, y **las citas no se pueden combinar con `output_config.format` (salidas estructuradas)**; la API devuelve un 400, así que esta aplicación nunca lo define. El texto citado no cuenta para los tokens de salida.

## Caché de prompts en `chat`

El mensaje de usuario de cada turno es `[new document blocks..., question]`. Los documentos recuperados en turnos anteriores se quedan exactamente donde estaban, y un seguimiento solo añade los fragmentos que aún no ha visto, de modo que el prefijo de la conversación es idéntico byte a byte y el caché puede acertar. El último bloque de documento de cada turno lleva `cache_control: {"type": "ephemeral"}` (se marcan los 3 turnos más recientes; la API permite 4 puntos de corte). Tras 24 fragmentos distintos, la sesión reinicia su conjunto de documentos para mantener acotado el contexto.

Límites honestos: un prefijo más corto que la longitud mínima cacheable del modelo (depende del modelo, aproximadamente de 1,000 a 4,000 tokens) simplemente no se cachea, y los 3 documentos de ejemplo están muy por debajo. El caché solo se nota (`cache_read > 0` en la línea de uso) con documentos más grandes. La duración por defecto del caché es de 5 minutos.

## Configuración de opciones

| Ajuste | Valor por defecto | Notas |
|---|---|---|
| `ANTHROPIC_API_KEY` | ninguno | necesario para `ask`/`chat`; nunca se imprime |
| `VOYAGE_API_KEY` | ninguno | solo para `--embed` / `--retriever voyage` |
| `--model` | `claude-sonnet-5-5` | cualquier modelo que admita citas; `claude-haiku-4-5` es más barato |
| `--chunk-size` / `--overlap` | 500 / 100 caracteres | fragmentos más pequeños dan citas más precisas |
| `-k/--top-k` | 4 | fragmentos enviados por pregunta |
| `PRICES` en `docqa/usage.py` | Sonnet 5.5 $2/$10, Haiku 4.5 $1/$5, Opus 5.5 $4/$20 por MTok | lecturas de caché al 10%, escrituras a 1.25x; es una estimación, revisa la página de precios |

No se usan parámetros de muestreo (`temperature`, etc.) ni prefill; los modelos actuales los rechazan.

## Notas de seguridad

- Los documentos son entrada no confiable. El prompt de sistema indica a Claude que trate el texto de los documentos como datos, pero la inyección de prompts a través de documentos no se puede prevenir por completo; no le des a esta aplicación herramientas que actúen sobre las respuestas.
- La clave se lee del entorno o de `.env` (en el `.gitignore`) y nunca se imprime. La salida del modelo solo se imprime, nunca se ejecuta.
- `ingest` solo lee las rutas que le pasas. Lo que sale de tu máquina es el texto de los fragmentos (no los archivos completos), hacia Anthropic y, con `--embed`, hacia Voyage AI.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest -q
```

27 pruebas sin conexión usan un cliente falso (`tests/conftest.py`) que registra las solicitudes y devuelve respuestas con la forma del SDK. Cubren la división en fragmentos, el ranking BM25, la presentación de citas, guardar y cargar el índice, las rutas de "la respuesta no está en los documentos", el rechazo y `max_tokens`, la estabilidad del prefijo y las marcas de caché en el chat, el uso y el costo, el recuperador de Voyage (con un embedder inyectado) y la CLI.

## Límites y lo que no se verificó en vivo

- No se hizo ninguna llamada a la API real durante la construcción; la forma de las solicitudes y respuestas se comprobó contra los tipos del SDK `anthropic` instalado y las notas del curso, no contra el servicio real.
- La extracción real de texto de PDF no se ejercitó en las pruebas (la lógica de página a fragmento se prueba con un lector simulado). Los PDF se dividen como texto extraído, así que los PDF escaneados, las tablas y los diseños no funcionan, y no se usa el modo PDF nativo de Claude (citas a nivel de página).
- BM25 usa un stemmer de plurales básico y stopwords en inglés. El índice JSON se carga completo en memoria.
- La calidad de la recuperación limita la calidad de la respuesta: si el fragmento correcto no está entre los top-k, Claude dirá que los documentos no contienen la respuesta.
- El historial del chat conserva solo el texto de las respuestas (no los bloques de citas), y no se usan las opciones de respaldo ante rechazos de Anthropic.

## Amplíalo

- Añade un paso de reordenamiento (recupera 20 y deja que Claude Haiku 4.5 elija los 4 mejores).
- Recuperación híbrida: combina los rankings de BM25 y Voyage (fusión de rangos recíprocos).
- Envía los PDF de forma nativa como bloques `document` en base64 para obtener citas a nivel de página.
- Transmite las respuestas con `client.messages.stream`.
- Cambia el índice JSON por una base de datos vectorial ([4.10](../../modulos/modulo4_aplicaciones/10_bases_datos_vectoriales.md)).
- Registra hashes de archivos para una ingesta incremental y no volver a calcular embeddings de archivos sin cambios.
