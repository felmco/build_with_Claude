"""CLI entry point: python main.py "your question"  (add --offline-demo to run with no API key)."""
from __future__ import annotations

import argparse
import asyncio
import os
import sys

import anthropic
from dotenv import load_dotenv

from research.budget import Budget
from research.fake import FakeClient
from research.pipeline import Config, ResearchError, run_research
from research.tools import build_tools

DEMO_QUESTION = "Does remote work improve productivity?"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Multi-agent web research assistant (lead + parallel workers + synthesizer).")
    p.add_argument("question", nargs="?", help="research question")
    p.add_argument("--model", default="claude-sonnet-5-5", help="lead/synthesizer model (default: %(default)s)")
    p.add_argument("--worker-model", default="claude-haiku-4-5",
                   help="worker model (default: %(default)s; Haiku uses the basic web tools, "
                        "Sonnet/Opus 4.6+ use dynamic-filtering web tools)")
    p.add_argument("--concurrency", type=int, default=3, help="max parallel workers (default: %(default)s)")
    p.add_argument("--max-searches", type=int, default=4, help="web_search max_uses per worker")
    p.add_argument("--max-fetches", type=int, default=3, help="web_fetch max_uses per worker")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--allowed-domains", nargs="+", metavar="DOMAIN", help="only search/fetch these domains")
    g.add_argument("--blocked-domains", nargs="+", metavar="DOMAIN", help="never search/fetch these domains")
    p.add_argument("--max-total-tokens", type=int, default=400_000, help="budget: input+output tokens (default: %(default)s)")
    p.add_argument("--max-cost", type=float, default=1.00, help="budget: estimated USD (default: %(default)s)")
    p.add_argument("--max-tool-uses", type=int, default=40, help="budget: searches+fetches in total (default: %(default)s)")
    p.add_argument("--out-dir", default="reports", help="where reports are saved (default: %(default)s)")
    p.add_argument("--offline-demo", action="store_true", help="run the full pipeline on canned fake data (no key, no network)")
    p.add_argument("--dry-run", action="store_true", help="print the configuration and tool definitions, make no API calls")
    p.add_argument("--quiet", action="store_true", help="no progress output")
    return p


def progress_printer(quiet: bool):
    if quiet:
        return lambda _m: None
    return lambda m: print(m, file=sys.stderr, flush=True)


def main(argv=None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    question = args.question or (DEMO_QUESTION if args.offline_demo else None)
    if not question:
        print("error: a question is required (or use --offline-demo)", file=sys.stderr)
        return 2
    if min(args.concurrency, args.max_searches, args.max_fetches) < 1:
        print("error: --concurrency, --max-searches and --max-fetches must be >= 1", file=sys.stderr)
        return 2

    cfg = Config(lead_model=args.model, worker_model=args.worker_model, concurrency=args.concurrency,
                 max_searches=args.max_searches, max_fetches=args.max_fetches,
                 allowed_domains=args.allowed_domains or [], blocked_domains=args.blocked_domains or [],
                 out_dir=args.out_dir)
    budget = Budget(args.max_total_tokens, args.max_cost, args.max_tool_uses)

    if args.dry_run:
        print(f"question: {question}\nlead/synthesizer: {cfg.lead_model}\nworkers: {cfg.worker_model} x{cfg.concurrency}")
        print(f"budget: {budget.max_tokens:,} tokens, ${budget.max_cost_usd:.2f}, {budget.max_tool_uses} tool uses")
        for t in build_tools(cfg.worker_model, cfg.max_searches, cfg.max_fetches, args.allowed_domains, args.blocked_domains):
            print("worker tool:", t)
        return 0

    if args.offline_demo:
        client = FakeClient()
        print("OFFLINE DEMO: using canned fictional data, no API calls.", file=sys.stderr)
    else:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("error: set ANTHROPIC_API_KEY (see .env.example) or try --offline-demo", file=sys.stderr)
            return 2
        client = anthropic.AsyncAnthropic(timeout=300.0)  # SDK retries 429/5xx twice by default

    try:
        result = asyncio.run(run_research(question, cfg, client, budget, progress_printer(args.quiet)))
    except ResearchError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except anthropic.AuthenticationError:
        print("error: authentication failed; check ANTHROPIC_API_KEY", file=sys.stderr)
        return 1
    except anthropic.APIError as e:
        print(f"error: API call failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    for w in result.warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(f"Report saved to {result.path}")
    print(result.budget.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
