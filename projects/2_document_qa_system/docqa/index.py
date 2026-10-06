"""On-disk index: a plain JSON file holding chunks (and optional embeddings).

JSON keeps the index human-readable and dependency-free. Fine for thousands of
chunks; beyond that, use a real vector database (see README).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .chunking import Chunk

INDEX_VERSION = 1


class IndexLoadError(Exception):
    """Raised for missing or unreadable indexes."""


@dataclass
class Index:
    chunks: list[Chunk]
    embeddings: list[list[float]] | None = None   # parallel to chunks
    embedding_model: str | None = None
    meta: dict = field(default_factory=dict)

    def documents(self) -> list[str]:
        return sorted({c.doc for c in self.chunks})

    def save(self, path: str | Path) -> None:
        data = {
            "version": INDEX_VERSION,
            "meta": self.meta,
            "chunks": [c.to_dict() for c in self.chunks],
            "embedding_model": self.embedding_model,
            "embeddings": self.embeddings,
        }
        Path(path).write_text(json.dumps(data), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Index":
        p = Path(path)
        if not p.exists():
            raise IndexLoadError(f"Index not found: {p}. Build one with: python main.py ingest data/")
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("version") != INDEX_VERSION:
                raise IndexLoadError(f"Unsupported index version {data.get('version')!r}; re-run ingest.")
            chunks = [Chunk.from_dict(d) for d in data["chunks"]]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise IndexLoadError(f"Index file {p} is corrupt ({exc}); re-run ingest.") from exc
        emb = data.get("embeddings")
        if emb is not None and len(emb) != len(chunks):
            raise IndexLoadError("Index embeddings do not match chunks; re-run ingest.")
        return cls(chunks, emb, data.get("embedding_model"), data.get("meta", {}))
