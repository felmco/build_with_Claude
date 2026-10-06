"""Structured findings: schema, validation, markdown, exit code, GitHub payload.

Lesson link: modules/module6_platform_features/02_structured_outputs_and_refusals.md
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict

from .diffparse import DiffFile

SEVERITIES = ["info", "low", "medium", "high", "critical"]   # ascending
CATEGORIES = ["bug", "security", "performance", "style", "test"]

# Passed as output_config={"format": {"type": "json_schema", "schema": ...}}.
# Structured outputs need additionalProperties:false and every key required;
# "no line" is expressed as 0 because the schema subset has no optional ints here.
FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "findings": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "file": {"type": "string"},
                "line": {"type": "integer"},
                "severity": {"type": "string", "enum": SEVERITIES},
                "category": {"type": "string", "enum": CATEGORIES},
                "message": {"type": "string"},
                "suggestion": {"type": "string"},
            },
            "required": ["file", "line", "severity", "category", "message", "suggestion"],
            "additionalProperties": False,
        }},
    },
    "required": ["summary", "findings"],
    "additionalProperties": False,
}

_CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def clean(s) -> str:
    """Model text may echo attacker-controlled repo content: strip control/ANSI bytes."""
    return _CTRL.sub("", str(s))


@dataclass
class Finding:
    file: str
    line: int
    severity: str
    category: str
    message: str
    suggestion: str


@dataclass
class Report:
    summary: str
    findings: list[Finding]


def parse_report(text: str) -> Report:
    """Validate the model's JSON ourselves too; the schema is a guarantee, not a reason to trust."""
    try:
        data = json.loads(text)
        items = data["findings"]
        findings = []
        for it in items:
            if it["severity"] not in SEVERITIES or it["category"] not in CATEGORIES:
                raise ValueError("enum value out of range")
            findings.append(Finding(clean(it["file"]), int(it["line"]), it["severity"], it["category"],
                                    clean(it["message"]), clean(it["suggestion"])))
        return Report(clean(data["summary"]), findings)
    except (ValueError, KeyError, TypeError) as e:
        raise ValueError(f"model output did not match the findings schema: {e}") from None


def sorted_findings(report: Report) -> list[Finding]:
    return sorted(report.findings, key=lambda f: (-SEVERITIES.index(f.severity), f.file, f.line))


def exit_code(report: Report, fail_on: str = "high") -> int:
    """0 = clean at the chosen threshold, 1 = at least one finding >= fail_on. 'none' never fails."""
    if fail_on == "none":
        return 0
    limit = SEVERITIES.index(fail_on)
    return 1 if any(SEVERITIES.index(f.severity) >= limit for f in report.findings) else 0


def render_markdown(report: Report) -> str:
    fs = sorted_findings(report)
    out = ["# Code review", "", report.summary, ""]
    if not fs:
        return "\n".join(out + ["No findings."])
    counts = {s: sum(f.severity == s for f in fs) for s in reversed(SEVERITIES)}
    out.append("**Findings:** " + ", ".join(f"{n} {s}" for s, n in counts.items() if n))
    for f in fs:
        loc = f"{f.file}:{f.line}" if f.line > 0 else f.file
        out += ["", f"### [{f.severity.upper()}] {f.category}: `{loc}`", "", f.message]
        if f.suggestion.strip():
            out += ["", f"**Suggestion:** {f.suggestion}"]
    return "\n".join(out)


def render_json(report: Report) -> str:
    return json.dumps({"summary": report.summary, "findings": [asdict(f) for f in sorted_findings(report)]}, indent=2)


def build_review_payload(report: Report, diff_files: dict[str, DiffFile], commit_id: str | None = None) -> dict:
    """Body for POST /repos/{owner}/{repo}/pulls/{n}/reviews (see README: shape NOT verified live).

    Inline comments only for lines visible on the new side of the diff; GitHub
    rejects others, so those go into the review body. event is always COMMENT:
    the bot never approves or requests changes.
    """
    inline, rest = [], []
    for f in sorted_findings(report):
        df = diff_files.get(f.file)
        text = f"**[{f.severity}/{f.category}]** {f.message}" + (f"\n\nSuggestion: {f.suggestion}" if f.suggestion.strip() else "")
        if df and f.line in df.visible_lines():
            inline.append({"path": f.file, "line": f.line, "side": "RIGHT", "body": text})
        else:
            rest.append(f"- `{f.file}:{f.line}` {text}")
    body = "Automated review (AI-generated, may be wrong).\n\n" + report.summary
    if rest:
        body += "\n\nFindings not attached to a diff line:\n" + "\n".join(rest)
    payload = {"body": body, "event": "COMMENT", "comments": inline}
    if commit_id:
        payload["commit_id"] = commit_id
    return payload
