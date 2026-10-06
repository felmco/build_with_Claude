"""Chunking: split a long text into overlapping pieces.

Why chunk? Retrieval works on small passages, and Claude's citations point at
passages, so smaller chunks give tighter, more checkable citations.
Why overlap? A fact that straddles a boundary still appears whole in one chunk.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Chunk:
    """One retrievable passage plus enough metadata to point back at the source."""
    id: str            # "<doc_id>#<n>"
    doc: str           # source file name (e.g. "refund_policy.md")
    text: str
    start: int         # char offset of the chunk in its source text (or page)
    end: int
    page: int | None = None  # 1-indexed PDF page, None for txt/md

    def location(self) -> str:
        where = f"chars {self.start}-{self.end}"
        return f"page {self.page}, {where}" if self.page else where

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Chunk":
        return cls(**d)


def split_text(text: str, size: int = 500, overlap: int = 100) -> list[tuple[int, int]]:
    """Return (start, end) spans covering `text`, each <= size chars, overlapping.

    Cuts prefer paragraph breaks, then sentence ends, then spaces, so chunks
    rarely stop mid-word.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must satisfy 0 <= overlap < size")
    spans: list[tuple[int, int]] = []
    n, pos = len(text), 0
    while pos < n:
        end = min(pos + size, n)
        if end < n:
            window_start = pos + size // 2  # never cut before half a chunk
            for sep in ("\n\n", ". ", "\n", " "):
                cut = text.rfind(sep, window_start, end)
                if cut != -1:
                    end = cut + len(sep)
                    break
        if text[pos:end].strip():
            spans.append((pos, end))
        if end >= n:
            break
        pos = max(end - overlap, pos + 1)  # always make progress
    return spans


def chunk_document(doc: str, text: str, size: int = 500, overlap: int = 100,
                   page: int | None = None, start_index: int = 0) -> list[Chunk]:
    """Chunk one text (or one PDF page) into Chunk objects."""
    chunks = []
    for i, (s, e) in enumerate(split_text(text, size, overlap), start=start_index):
        chunks.append(Chunk(id=f"{doc}#{i}", doc=doc, text=text[s:e], start=s, end=e, page=page))
    return chunks
