"""Source registry, citation renumbering and safe report saving."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .tools import safe_url

CITE = re.compile(r"\[(\d+)\]")


def normalize_url(url: str) -> str:
    """Dedupe key: lowercase scheme/host, drop fragment and trailing slash."""
    p = urlsplit(url.strip())
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/"), p.query, ""))


class SourceRegistry:
    """Gives every distinct URL one stable number across all workers."""

    def __init__(self):
        self._ids: dict[str, int] = {}
        self.items: list[dict] = []   # index = number - 1

    def add(self, url: str, title: str = "") -> int:
        key = normalize_url(url)
        if key not in self._ids:
            self.items.append({"url": url, "title": (title or url).strip()})
            self._ids[key] = len(self.items)
        return self._ids[key]

    def listing(self) -> list[str]:
        return [f"[{i}] {s['title']} - {s['url']}" for i, s in enumerate(self.items, 1)]


def finalize_report(markdown: str, registry: SourceRegistry) -> tuple[str, list[dict]]:
    """Renumber citations by first appearance, mark unknown ones, append a Sources section.

    The model cites with registry numbers; we do not trust it to build the Sources list.
    Numbers that are not in the registry (hallucinated) become [unverified].
    Only sources actually cited are listed.
    """
    order: dict[int, int] = {}

    def repl(m):
        n = int(m.group(1))
        if not (1 <= n <= len(registry.items)):
            return "[unverified]"
        order.setdefault(n, len(order) + 1)
        return f"[{order[n]}]"

    body = CITE.sub(repl, markdown).rstrip()
    cited = [registry.items[old - 1] for old in order]
    lines = ["", "## Sources", ""]
    if cited:
        lines += [f"{i}. [{_esc(s['title'])}]({s['url']})" if safe_url(s["url"]) else f"{i}. {_esc(s['title'])}"
                  for i, s in enumerate(cited, 1)]
    else:
        lines.append("_No citations were produced._")
    lines += ["", "> Sources are web pages the research agents retrieved; their content is untrusted "
              "and was not independently verified."]
    return body + "\n" + "\n".join(lines) + "\n", cited


def _esc(text: str) -> str:
    return re.sub(r"[\[\]\n\r]", " ", text).strip()


def slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:max_len].strip("-")
    return slug or "report"


def save_report(markdown: str, question: str, out_dir: str | Path = "reports") -> Path:
    """Write reports/<slug>.md. The slug is [a-z0-9-] only, so the path cannot escape out_dir."""
    out = Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    path = (out / f"{slugify(question)}.md").resolve()
    if path.parent != out:  # defence in depth
        raise ValueError("refusing to write outside the reports directory")
    path.write_text(markdown, encoding="utf-8")
    return path


def fallback_report(question: str, findings, registry: SourceRegistry, reason: str) -> str:
    """Raw-findings report used when the synthesizer cannot run (budget, refusal). No model call."""
    parts = [f"# {question}", "", f"> The synthesizer did not run ({reason}). Below are the raw worker "
             "findings; citation numbers refer to the Sources list.", ""]
    for f in findings:
        ids = "".join(f"[{registry.add(s['url'], s['title'])}]" for s in f.sources)
        parts += [f"## {f.question}", "", f.text or "_No findings._", "", f"Status: {f.status} {ids}", ""]
        if f.warnings:
            parts += ["Warnings: " + "; ".join(f.warnings), ""]
    return "\n".join(parts)
