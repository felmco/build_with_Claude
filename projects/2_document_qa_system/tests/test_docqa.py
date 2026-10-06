import json

import pytest

from conftest import FakeClient, char_cite, response, text_block, usage
from docqa.chunking import chunk_document, split_text
from docqa.index import Index, IndexLoadError
from docqa.ingest import IngestError, ingest, load_file
from docqa.qa import NO_ANSWER, QASession, build_answer, document_block
from docqa.retrieval import BM25Retriever, EmbeddingsUnavailable, VoyageRetriever, cosine, make_retriever, tokenize
from docqa.usage import Usage


# ---------------------------------------------------------------- chunking
def test_chunks_overlap_and_cover_text():
    text = " ".join(f"word{i}" for i in range(200))
    spans = split_text(text, size=100, overlap=20)
    assert len(spans) > 1
    assert spans[0][0] == 0 and spans[-1][1] == len(text)
    for (s1, e1), (s2, e2) in zip(spans, spans[1:]):
        assert s2 < e1            # overlap
        assert s2 > s1            # progress
    assert all(e - s <= 100 for s, e in spans)


def test_chunk_offsets_match_text():
    text = "Alpha beta gamma.\n\nDelta epsilon zeta. " * 20
    for c in chunk_document("d.txt", text, size=120, overlap=30):
        assert text[c.start:c.end] == c.text


def test_chunking_validates_and_handles_short_or_empty():
    assert split_text("short", 100, 10) == [(0, 5)]
    assert split_text("   ", 100, 10) == []
    with pytest.raises(ValueError):
        split_text("x", 10, 10)


# ---------------------------------------------------------------- BM25
def test_bm25_ranks_relevant_chunk_first(retriever):
    hits = retriever.search("how many days to return for a refund?", k=3)
    assert hits[0][0].doc == "refund.md"
    assert [s for _, s in hits] == sorted((s for _, s in hits), reverse=True)


def test_bm25_no_match_returns_empty(retriever):
    assert retriever.search("quantum chromodynamics", k=3) == []


def test_bm25_rare_term_beats_common_and_plural_stemming():
    from docqa.chunking import Chunk
    cs = [Chunk(f"d#{i}", "d", t, 0, len(t)) for i, t in enumerate(
        ["the cat sat on the mat", "the cat chased a zeppelin", "the cat and the cat"])]
    assert BM25Retriever(cs).search("zeppelin cat", 1)[0][0].id == "d#1"
    assert tokenize("Refunds are processed") == ["refund", "processed"]


# ---------------------------------------------------------------- index
def test_index_save_load_roundtrip(tmp_path, index):
    index.embeddings, index.embedding_model = [[0.1, 0.2]] * 3, "voyage-3.5"
    path = tmp_path / "i.json"
    index.save(path)
    loaded = Index.load(path)
    assert loaded.chunks == index.chunks
    assert loaded.embeddings == index.embeddings and loaded.embedding_model == "voyage-3.5"
    assert loaded.documents() == ["refund.md", "ship.txt", "warranty.md"]


def test_index_load_errors(tmp_path):
    with pytest.raises(IndexLoadError, match="not found"):
        Index.load(tmp_path / "nope.json")
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with pytest.raises(IndexLoadError, match="corrupt"):
        Index.load(bad)
    bad.write_text(json.dumps({"version": 99, "chunks": []}))
    with pytest.raises(IndexLoadError, match="version"):
        Index.load(bad)


# ---------------------------------------------------------------- ingest
def test_ingest_directory_and_unsupported(tmp_path):
    (tmp_path / "a.md").write_text("# A\nhello world " * 5)
    (tmp_path / "b.txt").write_text("plain text")
    (tmp_path / "skip.csv").write_text("x,y")
    docs = {c.doc for c in ingest([str(tmp_path)])}
    assert docs == {"a.md", "b.txt"}
    with pytest.raises(IngestError, match="Unsupported"):
        load_file(tmp_path / "skip.csv")
    with pytest.raises(IngestError, match="not found"):
        ingest([str(tmp_path / "missing")])


def test_pdf_without_pypdf_gives_clear_error(tmp_path, monkeypatch):
    import builtins
    real = builtins.__import__

    def fake(name, *a, **k):
        if name == "pypdf":
            raise ImportError("no pypdf")
        return real(name, *a, **k)
    monkeypatch.setattr(builtins, "__import__", fake)
    f = tmp_path / "x.pdf"
    f.write_bytes(b"%PDF-1.4")
    with pytest.raises(IngestError, match="pip install pypdf"):
        load_file(f)


def test_pdf_pages_become_chunks_with_page_numbers(tmp_path, monkeypatch):
    import docqa.ingest as ing
    monkeypatch.setattr(ing, "read_pdf_pages", lambda p: ["First page text.", "", "Third page text."])
    chunks = load_file(tmp_path / "r.pdf")
    assert [(c.page, c.id) for c in chunks] == [(1, "r.pdf#0"), (3, "r.pdf#1")]
    assert chunks[1].location().startswith("page 3")


# ---------------------------------------------------------------- request shape
def test_document_block_shape(chunks):
    b = document_block(chunks[0], cache=True)
    assert b["type"] == "document"
    assert b["source"] == {"type": "text", "media_type": "text/plain", "data": chunks[0].text}
    assert b["citations"] == {"enabled": True}
    assert b["cache_control"] == {"type": "ephemeral"}
    assert "cache_control" not in document_block(chunks[0])


def test_request_has_docs_system_and_no_output_format(retriever):
    client = FakeClient(response([text_block("30 days.", [char_cite(0, "within 30 days")])]))
    QASession(client, retriever).ask("refund days")
    req = client.calls[0]
    assert "output_config" not in req          # citations are incompatible with structured outputs
    assert req["model"] == "claude-sonnet-5-5" and req["max_tokens"] > 0
    assert "temperature" not in req
    content = req["messages"][0]["content"]
    assert content[0]["type"] == "document" and content[-1] == {"type": "text", "text": "refund days"}
    assert content[-2]["cache_control"] == {"type": "ephemeral"}   # last doc block cached


# ---------------------------------------------------------------- citation rendering
def test_citations_rendered_with_numbers_and_locations(chunks):
    resp = response([
        text_block("Returns are allowed "),
        text_block("within 30 days", [char_cite(0, "within 30 days", start=14, title="refund.md [chars 0-55]")]),
        text_block(" and shipping is 5 dollars.", [char_cite(1, "costs 5 dollars", start=50, title="ship.txt")]),
        text_block(" Again.", [char_cite(0, "within 30 days", start=14)]),   # duplicate source reuses [1]
    ])
    ans = build_answer(resp, chunks[:2])
    assert ans.text == "Returns are allowed within 30 days[1] and shipping is 5 dollars.[2] Again.[1]"
    assert [(s.num, s.cited_text) for s in ans.sources] == [(1, "within 30 days"), (2, "costs 5 dollars")]
    assert ans.sources[1].location == "chars 150-165"        # chunk.start(100) + 50
    out = ans.render()
    assert "Sources:" in out and '[1] refund.md [chars 0-55]  (chars 14-28)' in out


def test_non_text_blocks_ignored_and_citation_index_out_of_range(chunks):
    from types import SimpleNamespace as NS
    resp = response([NS(type="thinking", thinking="hmm"), text_block("ok", [char_cite(9, "x")])])
    ans = build_answer(resp, chunks)
    assert ans.text == "ok[1]" and ans.sources[0].location == "unknown location"


# ---------------------------------------------------------------- missing-answer behavior
def test_no_retrieval_hits_skips_api_call(retriever):
    client = FakeClient()
    ans = QASession(client, retriever).ask("quantum chromodynamics")
    assert client.calls == [] and not ans.answered and NO_ANSWER in ans.text
    assert "no API call" in ans.render()


def test_model_says_not_in_documents(retriever):
    client = FakeClient(response([text_block(NO_ANSWER)]))
    ans = QASession(client, retriever).ask("what is the refund policy for boats")
    assert not ans.answered and ans.sources == []
    assert NO_ANSWER in ans.render() and "No citations were returned" not in ans.render()


def test_system_prompt_requires_grounding_and_admitting_gaps(retriever):
    client = FakeClient(response([text_block("x")]))
    QASession(client, retriever).ask("refund")
    system = client.calls[0]["system"]
    assert "only the documents" in system and NO_ANSWER in system


def test_uncited_answer_is_flagged(retriever):
    client = FakeClient(response([text_block("Probably 30 days.")]))
    assert "No citations were returned" in QASession(client, retriever).ask("refund").render()


# ---------------------------------------------------------------- stop reasons
def test_refusal_and_max_tokens(retriever, chunks):
    ref = build_answer(response([], stop_reason="refusal"), chunks)
    assert not ref.answered and "declined" in ref.text
    cut = build_answer(response([text_block("partial")], stop_reason="max_tokens"), chunks)
    assert "max_tokens" in cut.note


# ---------------------------------------------------------------- chat + caching
def test_chat_followup_keeps_prefix_and_appends_only_new_docs(retriever):
    client = FakeClient(response([text_block("30 days.")]), response([text_block("5 dollars.")]))
    s = QASession(client, retriever, top_k=1)
    s.ask("refund days")
    s.ask("shipping cost dollars")
    first, second = client.calls[0]["messages"], client.calls[1]["messages"]
    assert second[0] == first[0]                         # identical cached prefix, byte for byte
    assert second[1] == {"role": "assistant", "content": "30 days."}
    docs2 = [b for b in second[2]["content"] if b["type"] == "document"]
    assert [d["source"]["data"] for d in docs2] == [s.pinned[1].text]   # only the new chunk
    assert len(s.pinned) == 2


def test_followup_with_no_new_hits_sends_no_documents(retriever):
    client = FakeClient(response([text_block("a")]), response([text_block("b")]))
    s = QASession(client, retriever, top_k=1)
    s.ask("refund days")
    s.ask("and the refund?")                 # same chunk retrieved again: already pinned
    assert not [b for b in client.calls[1]["messages"][2]["content"] if b["type"] == "document"]


def test_cache_marks_capped_and_disableable(retriever):
    s = QASession(FakeClient(), retriever)
    from docqa.qa import Turn
    turns = [Turn([c], f"q{i}") for i, c in enumerate(s.retriever.chunks * 2)]   # 6 doc turns
    marks = sum("cache_control" in b for m in s.build_messages(turns)
                if isinstance(m["content"], list) for b in m["content"])
    assert marks == 3
    s.use_cache = False
    assert not any("cache_control" in b for m in s.build_messages(turns) for b in m["content"])


# ---------------------------------------------------------------- usage
def test_usage_accumulates_and_estimates_cost(retriever):
    client = FakeClient(response([text_block("a")], u=usage(1000, 100, 0, 2000)),
                        response([text_block("b")], u=usage(100, 50, 2000, 0)))
    s = QASession(client, retriever)
    s.ask("refund days")
    s.ask("refund days")
    u = s.usage
    assert (u.input_tokens, u.output_tokens, u.cache_read, u.cache_write, u.requests) == (1100, 150, 2000, 2000, 2)
    expected = (1100 * 2 + 2000 * 2 * 0.1 + 2000 * 2 * 1.25 + 150 * 10) / 1e6
    assert u.cost("claude-sonnet-5-5") == pytest.approx(expected)
    assert "estimate" in u.summary("claude-sonnet-5-5")
    assert Usage().cost("unknown-model") is None


# ---------------------------------------------------------------- optional Voyage retriever
def test_voyage_retriever_with_injected_embedder(index):
    index.embeddings = [[1, 0], [0, 1], [1, 1]]
    r = VoyageRetriever(index, embed_query=lambda q: [0, 1])
    assert r.search("x", 1)[0][0].doc == "ship.txt"
    assert cosine([1, 0], [1, 0]) == pytest.approx(1.0)


def test_voyage_unavailable_errors_and_auto_fallback(index, monkeypatch):
    monkeypatch.delenv("VOYAGE_API_KEY", raising=False)
    with pytest.raises(EmbeddingsUnavailable):
        make_retriever(index, "voyage")
    index.embeddings = [[1, 0]] * 3
    with pytest.raises(EmbeddingsUnavailable, match="VOYAGE_API_KEY"):
        make_retriever(index, "voyage")
    assert isinstance(make_retriever(index, "auto"), BM25Retriever)


# ---------------------------------------------------------------- CLI
def test_cli_ingest_search_and_dry_run(tmp_path, capsys):
    import main
    idx = str(tmp_path / "i.json")
    data = str(__import__("pathlib").Path(main.__file__).parent / "data")
    assert main.main(["ingest", data, "--index", idx]) == 0
    assert main.main(["search", "how long is the warranty", "--index", idx]) == 0
    assert main.main(["ask", "warranty length", "--index", idx, "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "warranty_faq.md" in out and "no API call made" in out
    assert main.main(["ask", "x", "--index", str(tmp_path / "none.json"), "--dry-run"]) == 2
