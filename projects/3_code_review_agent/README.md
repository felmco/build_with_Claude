# 3 Code Review Agent

A command-line agent that reviews a code change. You give it a diff (file, local `git` range, or GitHub PR). Claude then explores the repository with **read-only, sandboxed tools** and returns **structured findings** (file, line, severity, category, message, suggestion). The CLI renders them as Markdown or JSON and sets an **exit code for CI**.

It never writes to your repo. It posts to GitHub only if you pass `--post`.

## Architecture

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

## Setup

```bash
cd projects/3_code_review_agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # add -r requirements-dev.txt for tests
cp .env.example .env                     # then put your key in .env (never commit it)
```

## Run

```bash
# Offline check of your input (no API call):
python main.py --diff examples/sample.diff --repo examples/sample_repo --dry-run

# Review the bundled sample (has a SQL injection and an off-by-one bug):
python main.py --diff examples/sample.diff --repo examples/sample_repo -v

# Review your own branch:
python main.py --git-range main..HEAD --repo . --fail-on medium

# Review a GitHub PR (dry run: prints the review payload it WOULD post):
python main.py --pr octocat/hello#123 --repo /path/to/local/checkout
# ...and really post inline comments (needs GITHUB_TOKEN with pull-request write access):
python main.py --pr octocat/hello#123 --repo /path/to/checkout --post
```

Expected output shape (stdout; the usage line goes to stderr):

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

(Real model output varies; I could not run it live while writing this.)

Exit codes: `0` nothing at or above `--fail-on` (default `high`; `none` never fails), `1` a finding at or above it, `2` bad input/config, `3` agent failure (refusal, truncated or invalid output, API error).

Options: `--model` (default `claude-sonnet-5-5`; try `claude-opus-5-5` for harder reviews), `--max-iterations` (max model calls, default 12), `--max-total-tokens` (soft cap, default 200000), `--format markdown|json`, `-v` (log tool calls), `--repo` (the sandbox root; for `--pr` it should be a checkout of the PR head).

## Claude features demonstrated

| Feature | Where | Lesson |
|---|---|---|
| Manual agent loop, `tool_use`/`tool_result`, all results in one message | `reviewer/agent.py` | [Agent loops](../../modules/module4_applications/06_agent_loops.md), [Tool use basics](../../modules/module3_advanced_features/01_tool_use_basics.md) |
| Tool design (schemas, errors as `is_error` results) | `reviewer/sandbox.py` | [Tool best practices](../../modules/module3_advanced_features/04_tool_best_practices.md) |
| Structured outputs `output_config.format` with tools, `refusal` / `max_tokens` handling | `reviewer/report.py`, `agent.py` | [Structured outputs and refusals](../../modules/module6_platform_features/02_structured_outputs_and_refusals.md) |
| Prompt-injection and sandbox security | system prompt, `sandbox.py` | [Security](../../modules/module5_optimization/21_security.md) |
| Usage and cost tracking | `reviewer/usage.py` | [Pricing and limits](../../modules/module1_foundation/03_pricing_limits.md) |
| Testing with a fake client | `tests/` | [Testing](../../modules/module4_applications/20_testing.md) |

More links: [REFERENCES.md](../../REFERENCES.md).

## Security notes

* **Repository contents are untrusted data.** A diff or file can contain text like "ignore previous instructions". The system prompt says so explicitly, tool output is wrapped in `<repo_data>` tags, and the model has no write or execute tools, so a successful injection can at worst skew the review. `examples/` contains such a comment on purpose. Treat the findings as advice, not as verified fact.
* **Sandbox:** paths are resolved (`..`, absolute paths, NUL bytes and symlinks pointing outside the root are rejected). `.env`, key files, `.git`, `node_modules` are never served. Caps on file size, lines per read, output size, grep matches and listing size.
* **Subprocess:** `git` runs with an argument list (no `shell=True`) after the range is validated against a strict pattern; 30 s timeout; output capped.
* **GitHub:** timeouts, no redirects followed, streamed size cap. The token is read from `GITHUB_TOKEN` and never printed. Reviews are always `event: COMMENT` (never approve or request changes). Model text is stripped of control characters before rendering.
* Keys are read from the environment only (`.env` is git-ignored).

## Honest limits

* **`--post` is unverified.** `docs.github.com` was blocked from the build environment, so the review payload (`POST /repos/{o}/{r}/pulls/{n}/reviews` with `body`, `event`, `comments[{path,line,side}]`, `commit_id`) was written from memory, and tested only against a mock transport. Compare it with the current GitHub docs and try it on a throwaway PR first. Without `--post` you only get the printed payload.
* Not run against the live Claude API. SDK call shapes were checked against the installed `anthropic` package (`messages.create` accepts `output_config`, `tool_choice`) and the skill docs, not by a real call.
* Findings on lines outside the diff cannot be inline comments; they go into the review body.
* `--max-total-tokens` is soft: it is checked between calls, so one call can overshoot. Input diffs over 200 KB are refused rather than truncated.
* `grep` uses Python `re` with length caps but no time limit, so a pathological regex can be slow.
* For `--pr`, tools read your *local* checkout, which may not match the PR head.
* The cost figure is an estimate from a small price table (cache reads priced at 10%; the real discount varies by model).

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q          # offline, uses a scripted fake Anthropic client (tests/conftest.py)
```

64 tests cover the sandbox (traversal, symlinks, size limits), git/PR input validation, the tool loop (parallel tools, tool errors, refusal, `max_tokens`, pause_turn, iteration and token caps), schema/Markdown rendering, exit codes, the GitHub payload and the CLI.

## Extend it

* Run per-file sub-reviews with `claude-haiku-4-5` workers and merge ([multi-agent](../../modules/module4_applications/07_multi_agent.md)).
* Add prompt caching to the system prompt and tools for big diffs ([caching](../../modules/module3_advanced_features/05_prompt_caching.md)).
* Load a team style guide as a tool, or SARIF output for code scanning.
* Post a single summary comment when `--post` would exceed rate limits; paginate large PRs.
