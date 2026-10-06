# 3 Agente de Revisión de Código

Un agente de línea de comandos que revisa un cambio de código. Le das un diff (archivo, rango local de `git` o PR de GitHub). Claude explora entonces el repositorio con **herramientas de solo lectura y aisladas en un sandbox** y devuelve **hallazgos estructurados** (archivo, línea, severidad, categoría, mensaje, sugerencia). La CLI los muestra en Markdown o JSON y establece un **código de salida para CI**.

Nunca escribe en tu repositorio. Solo publica en GitHub si pasas `--post`.

> Nota: los prompts del código (prompt de sistema, descripciones de herramientas) se mantienen en inglés para que el código y las pruebas sean idénticos a los de la versión en inglés. Puedes localizarlos a tu idioma si lo deseas.

## Arquitectura

```
 --diff FILE | --git-range A..B | --pr owner/repo#N
          |  (validated; git via argv list, no shell; size caps; httpx timeouts)
          v
      unified diff ──► parse_diff ──► files/hunks/visible lines
          |
          v
  ┌─────────────── Agent.review()  (manual loop, reviewer/agent.py) ───────────────┐
  │ messages.create(tools, output_config.format=JSON schema, system=injection warn)│
  │   stop_reason == tool_use ──► Sandbox.run_tool() ──► tool_result (is_error ok) │
  │   end_turn ──► parse + validate JSON      refusal / max_tokens ──► ReviewError │
  │ caps: --max-iterations (last call = wrap-up, tool_choice none), --max-total-tokens│
  └────────────────────────────────────────────────────────────────────────────────┘
          |                                   Sandbox: read_file, list_files, grep, get_diff_hunk
          v                                   (root-confined, symlink-safe, size-capped, read-only)
   Report ──► Markdown / JSON ──► stdout        usage summary + cost estimate ──► stderr
          ├──► exit code (0 / 1)
          └──► GitHub review payload ──► printed (dry run)  or POSTed with --post
```

## Configuración

```bash
cd es/proyectos/3_agente_revision_codigo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # añade -r requirements-dev.txt para las pruebas
cp .env.example .env                     # después pon tu clave en .env (nunca la subas al repositorio)
```

## Ejecución

```bash
# Comprobación offline de tu entrada (sin llamada a la API):
python main.py --diff examples/sample.diff --repo examples/sample_repo --dry-run

# Revisa el ejemplo incluido (tiene una inyección SQL y un error off-by-one):
python main.py --diff examples/sample.diff --repo examples/sample_repo -v

# Revisa tu propia rama:
python main.py --git-range main..HEAD --repo . --fail-on medium

# Revisa un PR de GitHub (dry run: imprime el payload de la revisión que PUBLICARÍA):
python main.py --pr octocat/hello#123 --repo /path/to/local/checkout
# ...y publica de verdad los comentarios en línea (necesita GITHUB_TOKEN con permiso de escritura en pull requests):
python main.py --pr octocat/hello#123 --repo /path/to/checkout --post
```

Forma esperada de la salida (stdout; la línea de uso va a stderr):

```
# Code review
<summary>
**Findings:** 1 high, 1 medium
### [HIGH] security: `app/db.py:15`
<message>
**Suggestion:** <fix>
...
usage: 4 calls, in=... out=... cache_read=... cache_write=... | ~$0.0xxx (estimate)
```

(La salida real del modelo varía; no pude ejecutarlo en vivo mientras escribía esto.)

Códigos de salida: `0` nada en `--fail-on` o por encima (por defecto `high`; `none` nunca falla), `1` hay un hallazgo en ese nivel o por encima, `2` entrada o configuración incorrecta, `3` fallo del agente (rechazo, salida truncada o inválida, error de la API).

Opciones: `--model` (por defecto `claude-sonnet-5-5`; prueba `claude-opus-5-5` para revisiones más difíciles), `--max-iterations` (máximo de llamadas al modelo, por defecto 12), `--max-total-tokens` (límite blando, por defecto 200000), `--format markdown|json`, `-v` (registra las llamadas a herramientas), `--repo` (la raíz del sandbox; con `--pr` debe ser un checkout del head del PR).

## Características de Claude demostradas

| Característica | Dónde | Lección |
|---|---|---|
| Bucle de agente manual, `tool_use`/`tool_result`, todos los resultados en un solo mensaje | `reviewer/agent.py` | [Bucles de agente](../../modulos/modulo4_aplicaciones/06_bucles_agente.md), [Fundamentos del uso de herramientas](../../modulos/modulo3_caracteristicas_avanzadas/01_conceptos_basicos_uso_herramientas.md) |
| Diseño de herramientas (esquemas, errores como resultados `is_error`) | `reviewer/sandbox.py` | [Mejores prácticas de herramientas](../../modulos/modulo3_caracteristicas_avanzadas/04_mejores_practicas_herramientas.md) |
| Salidas estructuradas `output_config.format` con herramientas, manejo de `refusal` / `max_tokens` | `reviewer/report.py`, `agent.py` | [Salidas estructuradas y rechazos](../../modulos/modulo6_caracteristicas_plataforma/02_salidas_estructuradas_rechazos.md) |
| Seguridad frente a inyección de prompts y sandbox | prompt de sistema, `sandbox.py` | [Seguridad](../../modulos/modulo5_optimizacion/21_seguridad.md) |
| Seguimiento de uso y costes | `reviewer/usage.py` | [Precios y límites](../../modulos/modulo1_fundamentos/03_precios_limites.md) |
| Pruebas con un cliente falso | `tests/` | [Pruebas](../../modulos/modulo4_aplicaciones/20_pruebas.md) |

Más enlaces: [REFERENCIAS.md](../../REFERENCIAS.md).

## Notas de seguridad

* **El contenido del repositorio son datos no confiables.** Un diff o un archivo puede contener texto como "ignore previous instructions". El prompt de sistema lo advierte explícitamente, la salida de las herramientas va envuelta en etiquetas `<repo_data>` y el modelo no tiene herramientas de escritura ni de ejecución, así que una inyección exitosa, como mucho, puede sesgar la revisión. `examples/` contiene un comentario así a propósito. Trata los hallazgos como consejos, no como hechos verificados.
* **Sandbox:** las rutas se resuelven (se rechazan `..`, rutas absolutas, bytes NUL y enlaces simbólicos que apunten fuera de la raíz). Nunca se sirven `.env`, archivos de claves, `.git` ni `node_modules`. Hay límites para el tamaño de archivo, las líneas por lectura, el tamaño de salida, las coincidencias de grep y el tamaño de los listados.
* **Subproceso:** `git` se ejecuta con una lista de argumentos (sin `shell=True`) después de validar el rango con un patrón estricto; timeout de 30 s; salida limitada.
* **GitHub:** timeouts, no se siguen redirecciones, límite de tamaño en streaming. El token se lee de `GITHUB_TOKEN` y nunca se imprime. Las revisiones son siempre `event: COMMENT` (nunca aprueban ni piden cambios). Al texto del modelo se le quitan los caracteres de control antes de mostrarlo.
* Las claves se leen solo del entorno (`.env` está ignorado por git).

## Límites honestos

* **`--post` no está verificado.** `docs.github.com` estaba bloqueado desde el entorno de construcción, así que el payload de la revisión (`POST /repos/{o}/{r}/pulls/{n}/reviews` con `body`, `event`, `comments[{path,line,side}]`, `commit_id`) se escribió de memoria y solo se probó contra un transporte simulado. Compáralo con la documentación actual de GitHub y pruébalo primero en un PR desechable. Sin `--post` solo obtienes el payload impreso.
* No se ha ejecutado contra la API real de Claude. Las formas de las llamadas del SDK se comprobaron contra el paquete `anthropic` instalado (`messages.create` acepta `output_config`, `tool_choice`) y la documentación de las skills, no con una llamada real.
* Los hallazgos en líneas fuera del diff no pueden ser comentarios en línea; van al cuerpo de la revisión.
* `--max-total-tokens` es blando: se comprueba entre llamadas, así que una llamada puede sobrepasarlo. Los diffs de entrada de más de 200 KB se rechazan en lugar de truncarse.
* `grep` usa `re` de Python con límites de longitud pero sin límite de tiempo, así que una regex patológica puede ser lenta.
* Con `--pr`, las herramientas leen tu checkout *local*, que puede no coincidir con el head del PR.
* La cifra de coste es una estimación a partir de una pequeña tabla de precios (lecturas de caché al 10 %; el descuento real varía según el modelo).

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest -q          # offline, usa un cliente falso de Anthropic con guion (tests/conftest.py)
```

64 pruebas cubren el sandbox (path traversal, enlaces simbólicos, límites de tamaño), la validación de entradas git/PR, el bucle de herramientas (herramientas en paralelo, errores de herramientas, rechazo, `max_tokens`, pause_turn, límites de iteraciones y tokens), el renderizado de esquema/Markdown, los códigos de salida, el payload de GitHub y la CLI.

## Amplíalo

* Ejecuta sub-revisiones por archivo con workers `claude-haiku-4-5` y fusiona los resultados ([multi-agente](../../modulos/modulo4_aplicaciones/07_multi_agente.md)).
* Añade caché de prompts al prompt de sistema y a las herramientas para diffs grandes ([caché](../../modulos/modulo3_caracteristicas_avanzadas/05_cache_prompt.md)).
* Carga una guía de estilo del equipo como herramienta, o salida SARIF para code scanning.
* Publica un único comentario de resumen cuando `--post` superaría los límites de tasa; pagina los PR grandes.
