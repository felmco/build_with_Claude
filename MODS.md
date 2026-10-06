# Claude Code Mod: "Consumo" (live usage pane)

A mod is a small plugin that draws inside Claude Code and hot-reloads. **Consumo** adds a pane that shows your current consumption while Claude works, like the "Consumo" card in the Claude Code screenshot that inspired it.

| Card | What it shows | Source |
|------|---------------|--------|
| TOKENS (último pedido) | Tokens in the context of the last response | `$.session.usage().context.tokens` |
| GASTO (API) | Session cost in USD | `$.session.usage().cost.usd` |
| CONTEXTO | % of the context window used, with a bar | `$.session.usage().context.percent` |
| HERRAMIENTAS | Tool calls this session, plus the last four tool names | `tool.call` hook |
| SESIÓN | mm:ss since the session started | `startedAt` and a 1-second clock |

The pane refreshes every second and on each prompt, tool call and finished turn. It shows "trabajando" while a turn runs.

## Use it

The mod lives in [`mods/consumo`](./mods/consumo).

```bash
claude --plugin-dir ./mods/consumo
```

Then type `/consumo` to open the pane. (In a session where hot reloading is enabled, put the folder under your dev-mods directory and it loads at the end of the turn.)

## Share it

Add a marketplace file beside `plugin.json` and install with `/plugin install consumo --marketplace <owner>/<repo>`.

## How it works

- `hooks/register.tsx` registers the `/consumo` command, opens a `Pane`, and keeps a snapshot in `$.state` (`types/index.d.ts` declares its shape).
- `ui.render` draws the cards with `Box` and `Text`.
- Check it with `claude plugin validate mods/consumo` and `claude plugin test mods/consumo`.

Read more: [Claude Code docs](https://code.claude.com/docs/en/overview) and the [Claude Academy](https://academy.claude.com/courses) "Claude Code in Action" course.
