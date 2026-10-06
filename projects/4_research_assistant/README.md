# 4 Research Assistant

A multi-agent research CLI. A **lead** agent splits your question into 3-5 sub-questions, **worker** agents research them in parallel with Anthropic's server-side web search and web fetch tools, and a **synthesizer** writes a markdown report with numbered citations, a Sources section and a section that flags conflicting or low-confidence claims. The report is saved to `reports/<slug>.md`.

```
python main.py "How effective are heat pumps in cold climates?"
python main.py --offline-demo        # whole pipeline on canned data, no key, no network
```

## Architecture

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

Files: `main.py` (CLI), `research/agents.py` (plan, worker, synthesizer), `research/tools.py` (tool versions, reading result blocks), `research/budget.py` (usage + guard + `PRICES`), `research/report.py` (citations, saving), `research/pipeline.py` (orchestration), `research/fake.py` (offline `FakeClient` and test builders).

## Setup

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # add requirements-dev.txt for pytest
cp .env.example .env                     # then put your key in .env
```

## Run

```
python main.py "What do we know about intermittent fasting and longevity?"
python main.py "Rust vs Go for CLI tools" --worker-model claude-sonnet-5-5 --max-cost 2
python main.py "EU AI Act obligations" --allowed-domains europa.eu eur-lex.europa.eu
python main.py "question" --dry-run      # show config and tool definitions, no API calls
```

Progress goes to stderr (`--quiet` hides it), then stdout ends with the report path and a usage line:

```
[lead:claude-sonnet-5-5] planning sub-questions
  1. Background: ...
[worker 1/3] searching: ...
[worker 1/3] ok, 5 sources (1/3 done, ~$0.041 so far)
...
Report saved to reports/how-effective-are-heat-pumps-in-cold-climates.md
Usage: 12 API calls, 85,000 in / 9,000 out (+0 cache read, 0 cache write), 14 tool uses (9 searches); estimated cost ~$0.2100 [...] (estimate, check your Console)
```

The `--offline-demo` content is fictional (`example.org` sources). It exists to show the flow: a `pause_turn` resume, a server-tool error block, conflicting claims, a bogus citation turned into `[unverified]`.

## Options

| Flag | Default | Meaning |
|---|---|---|
| `--model` | `claude-sonnet-5-5` | lead and synthesizer |
| `--worker-model` | `claude-haiku-4-5` | workers |
| `--concurrency` | 3 | parallel workers (semaphore) |
| `--max-searches` / `--max-fetches` | 4 / 3 | `max_uses` per worker |
| `--allowed-domains` / `--blocked-domains` | none | one or the other (the API rejects both) |
| `--max-total-tokens` / `--max-cost` / `--max-tool-uses` | 400000 / 1.00 / 40 | run budget |
| `--out-dir` | `reports` | output directory |

### Worker model trade-off

The `_20260209` web tools (dynamic filtering: the API runs code to trim pages before they enter context) need Sonnet 4.6+ / Opus 4.6+ class models. Haiku 4.5 is cheaper but gets the basic `web_search_20250305` / `web_fetch_20250910` versions, so pages enter context unfiltered and cost more tokens. `build_tools()` picks the version from the model name automatically. If answer quality or token cost on Haiku disappoints, try `--worker-model claude-sonnet-5-5`: it costs 2x per token but filters pages and reasons better.

## Claude features demonstrated

| Feature | Where | Lesson |
|---|---|---|
| Structured output with a JSON schema (`output_config.format`) | `agents.plan` | [6.2 Structured outputs and refusals](../../modules/module6_platform_features/02_structured_outputs_and_refusals.md) |
| Server tools: web search and fetch, `max_uses`, domain lists | `tools.build_tools` | [6.1 Server tools](../../modules/module6_platform_features/01_server_tools.md) |
| `pause_turn` resume, errors returned with HTTP 200 | `agents.run_worker`, `tools.server_tool_errors` | 6.1 |
| `stop_reason` handling: `refusal`, `max_tokens`, `pause_turn` | `agents.py` | 6.2 |
| Multi-agent orchestrator-worker pattern | `pipeline.py` | [4.7 Multi-agent](../../modules/module4_applications/07_multi_agent.md) |
| `AsyncAnthropic`, `asyncio.gather`, semaphore | `pipeline.py` | [5.12 Async concurrency](../../modules/module5_optimization/12_async_concurrency.md) |
| Usage tracking and cost estimate | `budget.py` | [1.3 Pricing](../../modules/module1_foundation/03_pricing_limits.md), [5.6 Token optimization](../../modules/module5_optimization/06_token_optimization.md) |
| Prompt-injection defence | prompts, `report.py` | [5.21 Security](../../modules/module5_optimization/21_security.md) |
| Testing with a fake client | `tests/` | [4.20 Testing](../../modules/module4_applications/20_testing.md) |

Official sources are in [REFERENCES.md](../../REFERENCES.md).

## Budget guard

`Budget.check()` runs before every API call and raises `BudgetExceeded` once tokens, estimated cost or tool uses reach the limit. A worker that hits it returns what it has with status `budget`; if the synthesizer cannot run, a raw-findings report is written without a model call. Limits are soft: requests already in flight (up to 3 workers) can overshoot, and cost uses the `PRICES` table in `research/budget.py` (cache reads at 10%, writes at 1.25x, searches at $0.01 each). It is an estimate, not your bill.

## Security notes

- Fetched web pages are untrusted and can contain prompt injection. Workers are told to treat content as evidence only; the synthesizer receives findings inside `<findings>` tags as data. This lowers the risk, it does not remove it.
- The workers have no client-side tools (no file or shell access), which limits what an injection can do. Do not add such tools without re-thinking this. Web fetch can only open URLs that already appeared in the conversation; use `--allowed-domains` for sensitive settings.
- Citation numbers are validated in code: the model never writes the Sources section, unknown numbers become `[unverified]`, and only `http(s)` URLs become links.
- The report filename is a `[a-z0-9-]` slug, so a question cannot write outside `--out-dir`.
- The API key is read from `ANTHROPIC_API_KEY` and is never printed. Keep `.env` out of git.

## Tests

```
pip install -r requirements-dev.txt
pytest -q
```

31 offline tests cover plan parsing and schema use, the `pause_turn` loop (resume shape, bound), tool versions per model, server-tool error blocks, refusal / `max_tokens` / API errors, the budget guard, citation renumbering, unsafe URLs, slug safety, semaphore concurrency, fallbacks, and the offline demo end to end.

## Limits

- Not run against the live API in this repo (no key during development). Request shapes were checked against the installed `anthropic` SDK and the course docs; expect to adjust on first live run. In particular, whether Haiku 4.5 accepts the basic fetch tool in your org and region is unverified here.
- Dynamic-filter tool versions `_20260209` are used for Sonnet/Opus; newer versions exist, check the tool reference.
- Workers run non-streaming with `max_tokens=4096`; long server-tool turns may be slow.
- On `pause_turn` the worker re-sends all assistant content so far. If the API turns out to return full content on resume, drop the accumulation in `run_worker`.
- Claims are only as good as the pages retrieved; the report flags conflicts but does not verify them.

## Extend it

- Stream progress per worker (`client.messages.stream`) for finer progress output.
- Add a critic agent that re-checks single-source claims with a second search.
- Cache the planner/synthesizer system prompts ([prompt caching](../../modules/module3_advanced_features/05_prompt_caching.md)).
- Use the Batch API for non-urgent research runs at half price.
- Retry failed workers once with a stronger model.
