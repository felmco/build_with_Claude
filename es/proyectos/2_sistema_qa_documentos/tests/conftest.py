"""Shared fakes: a fake Anthropic client returning canned, SDK-shaped responses."""
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from docqa.chunking import Chunk  # noqa: E402
from docqa.index import Index  # noqa: E402
from docqa.retrieval import BM25Retriever  # noqa: E402


def usage(i=100, o=20, read=0, write=0):
    return NS(input_tokens=i, output_tokens=o, cache_read_input_tokens=read,
              cache_creation_input_tokens=write)


def text_block(text, citations=None):
    return NS(type="text", text=text, citations=citations)


def char_cite(doc_index, cited, start=0, end=None, title="doc"):
    return NS(type="char_location", cited_text=cited, document_index=doc_index,
              document_title=title, start_char_index=start,
              end_char_index=end if end is not None else start + len(cited))


def response(blocks, stop_reason="end_turn", u=None):
    return NS(content=blocks, stop_reason=stop_reason, usage=u or usage())


class FakeClient:
    """Mimics `client.messages.create`; records every request, replays queued responses."""

    def __init__(self, *responses):
        self.queue = list(responses)
        self.calls = []
        self.messages = NS(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        return self.queue.pop(0)


@pytest.fixture
def chunks():
    return [
        Chunk("refund.md#0", "refund.md", "Items can be returned within 30 days for a full refund.", 0, 55),
        Chunk("ship.txt#0", "ship.txt", "Standard shipping takes 3 to 5 business days and costs 5 dollars.", 100, 165),
        Chunk("warranty.md#0", "warranty.md", "Electronics carry a 2-year limited warranty against defects.", 0, 60),
    ]


@pytest.fixture
def index(chunks):
    return Index(chunks)


@pytest.fixture
def retriever(chunks):
    return BM25Retriever(chunks)
