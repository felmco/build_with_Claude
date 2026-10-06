# 1. Customer Support Bot

A command-line support chatbot for a fictional shop ("Example Shop") built on the official `anthropic` Python SDK. It streams answers, looks things up in a small local knowledge base, opens tickets, escalates to a human, answers in the customer's language, and logs usage and cost for every turn.

## Architecture

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

Files: `main.py` (CLI), `support_bot/bot.py` (loop), `tools.py`, `history.py`, `analytics.py`, `prompts.py`, `offline.py` (dry-run stub), `tests/`.

## Setup

```bash
pip install -r requirements.txt            # add requirements-dev.txt for pytest
cp .env.example .env                       # then put your key in ANTHROPIC_API_KEY
python main.py --help
```

## Run

```bash
python main.py                    # claude-sonnet-5-5
python main.py --model claude-haiku-4-5       # cheaper (do not combine with --effort)
python main.py --effort low       # less thinking, faster, cheaper for simple chat
python main.py --dry-run          # offline demo with a stub "client": no key, no network
```

Expected shape of a session (text will differ):

```
You: Quiero devolver unos zapatos, ¿cuánto tarda el reembolso?
Aria: Puedes devolverlos en 30 días ... el reembolso llega en 5-7 días laborables ...
You: /stats
All time: 3 turns, 0 errors | tokens in=... out=... cache_read=... (hit rate 62%) | latency avg=2.10s p95=3.4s | tools: search_knowledge_base=2 | est. cost $0.0123
```

`--dry-run` replaces Claude with `support_bot/offline.py`, which is not an LLM: it searches the KB and quotes the best article. Use it to explore the REPL and tools, not to judge answer quality.

## Claude features demonstrated

| Feature | Where | Course lesson |
|---|---|---|
| Streaming (`client.messages.stream`, `text_stream`, `get_final_message`) | `bot.py` | [2.4 Streaming basics](../../modules/module2_core_api/04_streaming_basics.md), [2.5 Advanced](../../modules/module2_core_api/05_streaming_advanced.md) |
| System prompt, language rules, injection rules | `prompts.py` | [2.2 System prompts](../../modules/module2_core_api/02_system_prompts.md) |
| Conversation history and trimming | `history.py` | [2.3 Conversations](../../modules/module2_core_api/03_conversations.md) |
| Tool use, manual agent loop, parallel results in one message, `is_error` | `bot.py`, `tools.py` | [3.1 Tool use](../../modules/module3_advanced_features/01_tool_use_basics.md), [3.2 Custom tools](../../modules/module3_advanced_features/02_custom_tools.md), [4.6 Agent loops](../../modules/module4_applications/06_agent_loops.md) |
| Prompt caching (`cache_control` on last tool and on the system block) | `bot.py`, `tools.py` | [3.5 Prompt caching](../../modules/module3_advanced_features/05_prompt_caching.md) |
| Refusal and `max_tokens` handling | `bot.py` | [6.2 Structured outputs and refusals](../../modules/module6_platform_features/02_structured_outputs_and_refusals.md) |
| Usage tracking, cost estimate, JSONL logging | `analytics.py` | [1.3 Pricing](../../modules/module1_foundation/03_pricing_limits.md), [4.19 Logging](../../modules/module4_applications/19_logging_monitoring.md) |
| Prompt-injection hygiene, input limits | `bot.py`, `tools.py` | [5.21 Security](../../modules/module5_optimization/21_security.md) |
| Testing with a fake client | `tests/` | [4.20 Testing](../../modules/module4_applications/20_testing.md) |

Official docs: see [REFERENCES.md](../../REFERENCES.md) (tool use, prompt caching, streaming, errors).

## Configuration

| Option | Default | Meaning |
|---|---|---|
| `--model` | `claude-sonnet-5-5` | Any model ID. Cost estimates use the `PRICES` table in `analytics.py` (unknown models fall back to Sonnet prices). |
| `--max-tokens` | 1024 | Output cap per API call. |
| `--effort` | unset | `low`/`medium`/`high`, sent as `output_config.effort`. Not supported on Haiku 4.5. |
| `--kb`, `--tickets`, `--log` | `data/kb.json`, `data/tickets.jsonl`, `logs/analytics.jsonl` | File locations. |
| `--max-history` | 40 | Max messages kept (also capped at 40k characters in `history.py`). |
| `--dry-run` | off | Offline stub client. |

Environment: `ANTHROPIC_API_KEY` (read from the environment or `.env`; never printed).
Sampling parameters (`temperature` etc.), assistant prefill, and `budget_tokens` are not used; they are rejected by current models.

## Security notes

- **Untrusted KB text**: articles are returned inside `<knowledge_base_results>/<kb_document>` tags, `<` and `>` are escaped so text cannot close the tags, and the system prompt says to treat that content as data. This reduces, but does not eliminate, injection risk.
- **Tool arguments are untrusted**: validated (enums, email format, length caps); bad input returns `is_error: true` so Claude can correct itself. Nothing is executed as code or shell.
- **Input limits**: control characters stripped, empty or over 2000 characters rejected (never silently truncated).
- Tickets and the analytics log are plain files containing customer text and emails; they are git-ignored here. Apply your own retention and privacy policy before real use.
- The bot cannot issue refunds or verify identity; it only describes policy and opens tickets.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q          # 26 tests, offline, fake client in tests/conftest.py
```

They cover the streaming/tool loop, one-message tool results, caching parameters, refusal, `max_tokens`, API-error rollback, history trimming invariants, KB scoring and tag escaping, ticket validation, input limits, and cost math. The tests import `httpx2` (the HTTP library used by `anthropic` 1.x) to build a rate-limit error.

## Limits and honest caveats

- Not run against the live API in this repo's build environment: request shapes were checked against the installed SDK signatures and the official docs only. Please smoke-test with a real key.
- Caching only activates above a model-dependent minimum prefix (roughly 1-4k tokens). This small system prompt plus three tools may fall below it, so `cache_read` can stay at 0 until you grow the prompt or KB instructions. `/stats` shows whether it hits.
- Keyword scoring is crude (no stemming, no synonyms, English KB only; Claude translates queries). Replace it with embeddings (a third-party provider, since Anthropic has no embeddings endpoint) for a real KB.
- History trimming drops whole old turns without summarising them, so the bot forgets older context. It also changes the message prefix, so only the system and tools cache survives a trim.
- Thinking blocks (if the model emits any) are stored and replayed unchanged within a conversation.
- Cost figures are estimates from a hard-coded price table and may drift from the pricing page.
- Single user, single process, no persistence of conversations, no authentication.

## Extend it

- Swap keyword search for embeddings, or load KB from markdown files.
- Add `get_order_status` against a real order system (keep it read-only, check the caller's identity).
- Summarise trimmed turns, or use server-side compaction for long chats.
- Run a Haiku 4.5 triage step to route simple questions cheaply.
- Wrap `SupportBot` in a web or chat-platform handler; keep one `SupportBot` per customer.
