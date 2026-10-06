"""Orchestration: plan -> parallel workers (semaphore) -> synthesize -> save."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import anthropic

from .agents import Finding, PlanError, plan, run_worker, synthesize
from .budget import Budget, BudgetExceeded
from .report import SourceRegistry, fallback_report, finalize_report, save_report


class ResearchError(RuntimeError):
    pass


@dataclass
class Config:
    lead_model: str = "claude-sonnet-5-5"     # plans and synthesizes
    worker_model: str = "claude-haiku-4-5"    # cheap parallel searchers (basic web tools)
    concurrency: int = 3
    max_searches: int = 4
    max_fetches: int = 3
    max_continuations: int = 5
    allowed_domains: list = field(default_factory=list)
    blocked_domains: list = field(default_factory=list)
    out_dir: str = "reports"


@dataclass
class Result:
    question: str
    sub_questions: list
    findings: list
    markdown: str
    path: Path
    budget: Budget
    warnings: list


def _quiet(_msg: str) -> None:
    pass


async def run_research(question: str, cfg: Config, client, budget: Budget, progress=_quiet) -> Result:
    warnings: list[str] = []

    # 1. Plan (structured output)
    progress(f"[lead:{cfg.lead_model}] planning sub-questions")
    try:
        subs = await plan(client, budget, question, cfg.lead_model)
    except PlanError as e:
        warnings.append(f"planning failed ({e}); researching the question as a single task")
        subs = [question]
    for i, q in enumerate(subs, 1):
        progress(f"  {i}. {q}")

    # 2. Workers run concurrently; the semaphore caps simultaneous API calls (rate limits).
    sem = asyncio.Semaphore(cfg.concurrency)
    done = 0

    async def one(i: int, q: str) -> Finding:
        nonlocal done
        async with sem:
            progress(f"[worker {i}/{len(subs)}] searching: {q[:70]}")
            f = await run_worker(
                client, budget, q, cfg.worker_model, max_searches=cfg.max_searches,
                max_fetches=cfg.max_fetches, allowed_domains=cfg.allowed_domains or None,
                blocked_domains=cfg.blocked_domains or None, max_continuations=cfg.max_continuations)
        done += 1
        progress(f"[worker {i}/{len(subs)}] {f.status}, {len(f.sources)} sources "
                 f"({done}/{len(subs)} done, ~${budget.cost_usd:.3f} so far)")
        return f

    findings = list(await asyncio.gather(*(one(i, q) for i, q in enumerate(subs, 1))))
    for f in findings:
        warnings += [f"{f.question[:50]}...: {w}" for w in f.warnings]
    if not any(f.text for f in findings):
        raise ResearchError("no worker produced any findings; nothing to synthesize")

    # 3. Synthesize. If we cannot (budget/refusal/API error) fall back to the raw findings.
    registry = SourceRegistry()
    progress(f"[synthesizer:{cfg.lead_model}] writing report")
    try:
        body, w = await synthesize(client, budget, question, findings, registry, cfg.lead_model)
        warnings += w
    except (BudgetExceeded, PlanError, anthropic.APIError) as e:
        warnings.append(f"synthesis skipped: {e}")
        body = fallback_report(question, findings, registry, str(e))
    markdown, _ = finalize_report(body, registry)
    markdown += (f"\n---\n_Generated {date.today().isoformat()} by research_assistant "
                 f"(lead {cfg.lead_model}, workers {cfg.worker_model}). {budget.summary()}_\n")

    path = save_report(markdown, question, cfg.out_dir)
    progress(f"saved {path}")
    return Result(question, subs, findings, markdown, path, budget, warnings)
