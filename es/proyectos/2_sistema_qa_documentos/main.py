#!/usr/bin/env python3
"""Document Q&A (RAG) CLI: ingest -> index -> retrieve -> ask Claude with citations.

  python main.py ingest data/            # build index.json
  python main.py search "refund window"  # offline: see what retrieval finds
  python main.py ask "How long do I have to return an item?"
  python main.py chat                    # follow-ups reuse cached documents
"""
from __future__ import annotations

import argparse
import os
import sys

from docqa.index import Index, IndexLoadError
from docqa.ingest import IngestError, ingest
from docqa.qa import DEFAULT_MODEL, SYSTEM_PROMPT, QASession
from docqa.retrieval import EmbeddingsUnavailable, embed_texts, make_retriever, VOYAGE_MODEL

try:  # python-dotenv is optional at runtime
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def cmd_ingest(args) -> int:
    chunks = ingest(args.paths, args.chunk_size, args.overlap)
    index = Index(chunks, meta={"chunk_size": args.chunk_size, "overlap": args.overlap})
    if args.embed:
        vectors = embed_texts([c.text for c in chunks], "document", VOYAGE_MODEL)
        index.embeddings, index.embedding_model = vectors, VOYAGE_MODEL
    index.save(args.index)
    docs = index.documents()
    print(f"Indexed {len(chunks)} chunks from {len(docs)} document(s): {', '.join(docs)}")
    print(f"Index written to {args.index}" + (" (with Voyage embeddings)" if args.embed else ""))
    return 0


def _retriever(args):
    return make_retriever(Index.load(args.index), args.retriever)


def cmd_search(args) -> int:
    hits = _retriever(args).search(args.question, args.top_k)
    if not hits:
        print("No matching passages.")
    for rank, (c, score) in enumerate(hits, 1):
        snippet = " ".join(c.text.split())[:160]
        print(f"{rank}. {c.doc} ({c.location()}) score={score:.3f}\n   {snippet}...")
    return 0


def _make_session(args) -> QASession:
    retriever = _retriever(args)
    if args.dry_run:
        client = None
    else:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("ANTHROPIC_API_KEY is not set (put it in .env or export it). "
                             "Use --dry-run to try retrieval without the API.")
        import anthropic
        client = anthropic.Anthropic()  # SDK retries 429/5xx automatically
    return QASession(client, retriever, args.model, args.top_k, args.max_tokens,
                     use_cache=not args.no_cache)


def _dry_run(session: QASession, question: str) -> None:
    turn = session.plan_turn(question)
    print(f"[dry-run] model={session.model}, {len(turn.docs)} document block(s), no API call made.")
    for c in turn.docs:
        print(f"  - {c.doc} ({c.location()}), {len(c.text)} chars")
    if not turn.docs:
        print("  (no matches: a real run would answer 'not in the documents' without calling the API)")
    print(f"[dry-run] system prompt: {SYSTEM_PROMPT.splitlines()[0]}")


def _ask_once(session: QASession, question: str, show_usage: bool = True) -> None:
    import anthropic
    try:
        print(session.ask(question).render())
    except anthropic.RateLimitError:
        print("Rate limited by the API (after automatic retries). Try again shortly.", file=sys.stderr)
    except anthropic.APIConnectionError:
        print("Could not reach the API. Check your network connection.", file=sys.stderr)
    except anthropic.APIStatusError as exc:
        print(f"API error {exc.status_code}: {exc.message}", file=sys.stderr)
    else:
        if show_usage:
            print("\n" + session.usage.summary(session.model))
        return
    raise SystemExit(1)


def cmd_ask(args) -> int:
    session = _make_session(args)
    if args.dry_run:
        _dry_run(session, args.question)
        return 0
    _ask_once(session, args.question)
    return 0


def cmd_chat(args) -> int:
    session = _make_session(args)
    print(f"Chat over {len(Index.load(args.index).documents())} document(s). Empty line or 'exit' quits.")
    while True:
        try:
            q = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"", "exit", "quit"}:
            break
        if args.dry_run:
            _dry_run(session, q)
            continue
        _ask_once(session, q, show_usage=False)
    if session.usage.requests:
        print("\n" + session.usage.summary(session.model))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Document Q&A over your files, answered by Claude with citations.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, question=True):
        sp.add_argument("--index", default="index.json", help="index file (default: index.json)")
        sp.add_argument("--retriever", choices=["bm25", "voyage", "auto"], default="bm25",
                        help="bm25 (default, offline) | voyage (needs VOYAGE_API_KEY + voyageai + --embed index) | auto")
        sp.add_argument("-k", "--top-k", type=int, default=4, help="chunks to retrieve (default: 4)")
        if question:
            sp.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude model (default: {DEFAULT_MODEL})")
            sp.add_argument("--max-tokens", type=int, default=2048)
            sp.add_argument("--no-cache", action="store_true", help="disable prompt caching")
            sp.add_argument("--dry-run", action="store_true", help="retrieve only; make no API call")

    s = sub.add_parser("ingest", help="read txt/md/pdf files and build the index")
    s.add_argument("paths", nargs="+", help="files or directories")
    s.add_argument("--index", default="index.json")
    s.add_argument("--chunk-size", type=int, default=500, help="max characters per chunk")
    s.add_argument("--overlap", type=int, default=100, help="characters shared by neighbouring chunks")
    s.add_argument("--embed", action="store_true", help="also store Voyage AI embeddings (optional)")
    s.set_defaults(fn=cmd_ingest)

    s = sub.add_parser("search", help="show retrieved passages (offline, no Claude call)")
    s.add_argument("question")
    common(s, question=False)
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("ask", help="ask one question")
    s.add_argument("question")
    common(s)
    s.set_defaults(fn=cmd_ask)

    s = sub.add_parser("chat", help="interactive Q&A with prompt caching across follow-ups")
    common(s)
    s.set_defaults(fn=cmd_chat)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except (IngestError, IndexLoadError, EmbeddingsUnavailable, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
