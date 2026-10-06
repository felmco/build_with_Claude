# What's New in This Revision (October 2026)

This revision brings the course in line with the current Claude lineup and API. If you took an earlier version, these are the changes that matter.

## Models

| Old course examples | Now use |
|---------------------|---------|
| `claude-sonnet-4-5-20250929` | `claude-sonnet-5-5` ($2 / $10 per MTok, 1M context) |
| `claude-opus-4-5-20251101`, `claude-opus-4-1-20250805` | `claude-opus-5-5` ($4 / $20, 1M context) |
| `claude-3-5-haiku-20241022`, `claude-3-7-sonnet-20250219` | `claude-haiku-4-5` ($1 / $5, 200K) or `claude-sonnet-5-5` |
| (new) | `claude-fable-5-1` ($10 / $50) for the hardest long-horizon work |

Model IDs are now dateless pinned snapshots. Do not add date suffixes.

## API behaviour changes covered in the lessons

- **Thinking**: adaptive thinking plus `output_config.effort` replaces `budget_tokens` on the 5.x models (Haiku 4.5 keeps `budget_tokens`). Opus 5.5 defaults to `medium` effort.
- **Sampling parameters**: non-default `temperature`, `top_p`, `top_k` return a 400 on Fable 5.1, Opus 5.5 and Sonnet 5.5. The temperature exercise now runs on Haiku 4.5.
- **Prefill removed**: ending `messages` with an `assistant` turn returns a 400. Use structured outputs (`output_config.format`) or instructions.
- **Files API is GA**: `client.files.*`, no beta header.
- **Computer use**: `computer_toolset_20260801`, no beta header, replaces `computer_20251124`.
- **Limits**: 1M context and 128K output on Sonnet/Opus/Fable; always read limits from the Models API.
- **Pricing and caching tables** refreshed; cache reads are 5% on Opus 5.5 and 2.5% on Fable 5.1.

## New in the repo

- [REFERENCES.md](./REFERENCES.md): official docs and Claude Academy mapped to lessons.
- [MODS.md](./MODS.md) and [`mods/consumo`](./mods/consumo): a live usage pane for Claude Code (tokens, spend, context, tools, session time).
- Spanish mirrors: `es/REFERENCIAS.md`, `es/NOVEDADES.md`, `es/MODS.md`.

## Not yet covered (candidates for the next revision)

Managed Agents, the Claude Agent SDK, server-side tools such as web search/fetch and code execution, refusal fallbacks, task budgets and Admin API. See [REFERENCES.md](./REFERENCES.md) for their official docs.
