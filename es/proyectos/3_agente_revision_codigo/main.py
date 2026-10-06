#!/usr/bin/env python3
"""Code review agent CLI.  See README.md.

Exit codes: 0 ok / nothing at or above --fail-on, 1 findings at/above --fail-on,
2 bad input or configuration, 3 the agent failed (refusal, truncation, API error).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import anthropic
from dotenv import load_dotenv

from reviewer.agent import DEFAULT_MODEL, Agent, ReviewError
from reviewer.diffparse import parse_diff
from reviewer.ghpost import post_review
from reviewer.report import (SEVERITIES, build_review_payload, exit_code, render_json,
                             render_markdown)
from reviewer.sandbox import Sandbox, SandboxError
from reviewer.sources import (MAX_DIFF_BYTES, SourceError, fetch_pr, git_range_diff,
                              parse_pr_ref, read_diff_file)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Autonomous, read-only code review agent powered by Claude.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--diff", metavar="FILE", help="unified diff file")
    src.add_argument("--git-range", metavar="RANGE", help="e.g. main..HEAD (runs `git diff` in --repo)")
    src.add_argument("--pr", metavar="OWNER/REPO#N", help="GitHub PR (GITHUB_TOKEN optional for public repos)")
    p.add_argument("--repo", default=".", help="repo root the tools may read (default: .)")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"model id (default: {DEFAULT_MODEL})")
    p.add_argument("--max-iterations", type=int, default=12, help="max model calls (default 12)")
    p.add_argument("--max-total-tokens", type=int, default=200_000,
                   help="soft token cap; once reached the agent must wrap up (default 200000)")
    p.add_argument("--fail-on", choices=SEVERITIES + ["none"], default="high",
                   help="exit 1 if any finding is at/above this severity (default high)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--post", action="store_true",
                   help="actually POST inline comments to the PR (needs --pr and GITHUB_TOKEN). Default: dry run")
    p.add_argument("--dry-run", action="store_true", help="parse input and show the plan; make no API call")
    p.add_argument("-v", "--verbose", action="store_true", help="print each tool call to stderr")
    return p


def main(argv=None, client=None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    if args.post and not args.pr:
        print("error: --post only works with --pr", file=sys.stderr)
        return 2
    if args.max_iterations < 1 or args.max_total_tokens < 1000:
        print("error: --max-iterations must be >= 1 and --max-total-tokens >= 1000", file=sys.stderr)
        return 2
    token = os.environ.get("GITHUB_TOKEN") or None
    head_sha = None
    try:
        if args.diff:
            diff = read_diff_file(args.diff)
        elif args.git_range:
            diff = git_range_diff(args.git_range, args.repo)
        else:
            owner, repo, num = parse_pr_ref(args.pr)
            diff, head_sha = fetch_pr(owner, repo, num, token)
        sandbox = Sandbox(args.repo, diff_files=parse_diff(diff))
    except (SourceError, SandboxError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not diff.strip():
        print("error: the diff is empty", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"[dry-run] model={args.model} diff={len(diff)} bytes (cap {MAX_DIFF_BYTES}) "
              f"files={list(sandbox.diff_files)} max_iterations={args.max_iterations} "
              f"max_total_tokens={args.max_total_tokens}\n[dry-run] no API call made")
        return 0

    if client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("error: set ANTHROPIC_API_KEY (see .env.example)", file=sys.stderr)
            return 2
        client = anthropic.Anthropic(timeout=120.0)   # SDK retries 429/5xx itself
    agent = Agent(client, sandbox, model=args.model, max_iterations=args.max_iterations,
                  max_total_tokens=args.max_total_tokens)
    try:
        report = agent.review(diff)
    except ReviewError as e:
        print(f"error: review failed: {e}", file=sys.stderr)
        print(agent.usage.summary(args.model), file=sys.stderr)
        return 3
    except anthropic.APIError as e:
        print(f"error: API call failed: {e.__class__.__name__}", file=sys.stderr)
        return 3
    if args.verbose:
        for name, a in agent.tool_calls:
            print(f"[tool] {name} {json.dumps(a)[:150]}", file=sys.stderr)

    print(render_json(report) if args.format == "json" else render_markdown(report))

    if args.pr:
        payload = build_review_payload(report, sandbox.diff_files, head_sha)
        if args.post:
            try:
                url = post_review(owner, repo, num, payload, token)
                print(f"\nposted review: {url}", file=sys.stderr)
            except SourceError as e:
                print(f"error: {e}", file=sys.stderr)
                return 3
        else:
            print("\n[DRY RUN] would POST this review payload (pass --post to send it):\n"
                  + json.dumps(payload, indent=2), file=sys.stderr)
    print(agent.usage.summary(args.model), file=sys.stderr)
    return exit_code(report, args.fail_on)


if __name__ == "__main__":
    sys.exit(main())
