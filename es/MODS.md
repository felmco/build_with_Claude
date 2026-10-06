# Mod de Claude Code: "Consumo" (panel de uso en vivo)

Un mod es un pequeño plugin que dibuja dentro de Claude Code y se recarga en caliente. **Consumo** añade un panel que muestra tu consumo actual mientras Claude trabaja, como la tarjeta "Consumo" de la captura que lo inspiró.

| Tarjeta | Qué muestra | Origen |
|---------|-------------|--------|
| TOKENS (último pedido) | Tokens en el contexto de la última respuesta | `$.session.usage().context.tokens` |
| GASTO (API) | Coste de la sesión en USD | `$.session.usage().cost.usd` |
| CONTEXTO | % de la ventana de contexto usado, con barra | `$.session.usage().context.percent` |
| HERRAMIENTAS | Llamadas a herramientas y las últimas cuatro | hook `tool.call` |
| SESIÓN | mm:ss desde el inicio de la sesión | `startedAt` y un reloj de 1 s |

El panel se actualiza cada segundo y en cada prompt, herramienta y turno terminado, y muestra "trabajando" mientras corre un turno.

## Úsalo

El mod está en [`../mods/consumo`](../mods/consumo).

```bash
claude --plugin-dir ./mods/consumo
```

Escribe `/consumo` para abrir el panel.

## Compártelo

Añade un archivo de marketplace junto a `plugin.json` e instala con `/plugin install consumo --marketplace <owner>/<repo>`.

## Cómo funciona

- `hooks/register.tsx` registra el comando `/consumo`, abre un `Pane` y guarda una instantánea en `$.state` (`types/index.d.ts` declara su forma).
- `ui.render` dibuja las tarjetas con `Box` y `Text`.
- Compruébalo con `claude plugin validate mods/consumo` y `claude plugin test mods/consumo`.

Más información: [documentación de Claude Code](https://code.claude.com/docs/en/overview) y el curso "Claude Code in Action" de la [Claude Academy](https://academy.claude.com/courses).
