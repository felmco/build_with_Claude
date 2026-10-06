"""Retrieval: find the chunks most relevant to a question.

Default: pure-Python BM25 (keyword ranking, no services, no API keys).
Optional: Voyage AI embeddings. Anthropic does NOT offer an embeddings API,
so semantic retrieval needs a third-party provider such as Voyage AI.
"""
from __future__ import annotations

import math
import os
import re
from collections import Counter

from .chunking import Chunk
from .index import Index

STOPWORDS = frozenset(
    "a an and are as at be by can do does for from how i in is it of on or that the "
    "this to was what when where which who why will with you your".split()
)
_WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase, drop stopwords, and crudely stem plurals ('refunds' -> 'refund')."""
    out = []
    for w in _WORD.findall(text.lower()):
        if w in STOPWORDS:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(w)
    return out


class BM25Retriever:
    """Okapi BM25. score = sum over query terms of idf * tf*(k1+1) / (tf + k1*(1-b+b*len/avglen))."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.docs_tf = [Counter(tokenize(c.text)) for c in chunks]
        self.lengths = [sum(tf.values()) for tf in self.docs_tf]
        self.avg_len = (sum(self.lengths) / len(chunks)) if chunks else 0.0
        df: Counter = Counter()
        for tf in self.docs_tf:
            df.update(tf.keys())
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        """Top-k (chunk, score) with score > 0. An empty list means nothing matched."""
        q_terms = set(tokenize(query))
        scored = []
        for i, tf in enumerate(self.docs_tf):
            score = 0.0
            for t in q_terms:
                f = tf.get(t)
                if not f:
                    continue
                norm = f + self.k1 * (1 - self.b + self.b * self.lengths[i] / (self.avg_len or 1))
                score += self.idf[t] * f * (self.k1 + 1) / norm
            if score > 0:
                scored.append((self.chunks[i], score))
        scored.sort(key=lambda x: (-x[1], x[0].id))
        return scored[:k]


# ---------------------------------------------------------------- Voyage (optional)
VOYAGE_MODEL = "voyage-3.5"


class EmbeddingsUnavailable(Exception):
    pass


def _voyage_client():
    if not os.environ.get("VOYAGE_API_KEY"):
        raise EmbeddingsUnavailable("VOYAGE_API_KEY is not set (Voyage AI is a separate provider from Anthropic).")
    try:
        import voyageai
    except ImportError as exc:
        raise EmbeddingsUnavailable("The optional 'voyageai' package is missing: pip install voyageai") from exc
    return voyageai.Client()  # reads VOYAGE_API_KEY


def embed_texts(texts: list[str], input_type: str, model: str = VOYAGE_MODEL) -> list[list[float]]:
    client = _voyage_client()
    out: list[list[float]] = []
    for i in range(0, len(texts), 128):  # stay under per-request batch limits
        out += client.embed(texts[i:i + 128], model=model, input_type=input_type).embeddings
    return out


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class VoyageRetriever:
    """Cosine similarity over stored Voyage embeddings. `embed_query` is injectable for tests."""

    def __init__(self, index: Index, embed_query=None):
        if not index.embeddings:
            raise EmbeddingsUnavailable("This index has no embeddings. Re-run: python main.py ingest ... --embed")
        self.index = index
        self.embed_query = embed_query or (
            lambda q: embed_texts([q], "query", index.embedding_model or VOYAGE_MODEL)[0])

    def search(self, query: str, k: int = 4) -> list[tuple[Chunk, float]]:
        qv = self.embed_query(query)
        scored = [(c, cosine(qv, v)) for c, v in zip(self.index.chunks, self.index.embeddings)]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


def make_retriever(index: Index, kind: str = "bm25"):
    """kind: 'bm25' (default), 'voyage', or 'auto' (voyage if available, else bm25)."""
    if kind == "bm25":
        return BM25Retriever(index.chunks)
    if kind == "voyage":
        if not index.embeddings:
            raise EmbeddingsUnavailable("This index has no embeddings. Re-run ingest with --embed.")
        _voyage_client()  # fail early with a clear message
        return VoyageRetriever(index)
    if kind == "auto":
        try:
            return make_retriever(index, "voyage")
        except EmbeddingsUnavailable:
            return BM25Retriever(index.chunks)
    raise ValueError(f"unknown retriever {kind!r}")
