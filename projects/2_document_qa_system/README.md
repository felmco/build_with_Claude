# Project 2: Document Q&A (RAG) with citations

A command-line RAG app. It ingests your `.txt`, `.md` and (optionally) `.pdf` files, splits them into overlapping chunks, stores them in a JSON index, retrieves the best chunks for a question, and asks Claude to answer **only from those chunks**, with numbered citations back to the exact passage.

## Architecture

```
 ingest                                   ask / chat
 ------                                   ----------
 files (txt/md/pdf)                       question
   |  docqa/ingest.py                       |
   v                                        v
 chunks (500 chars, 100 overlap)          retriever  <-- BM25 (default, pure Python)
   |  docqa/chunking.py                       |           or Voyage embeddings (optional)
   v                                          v  top-k chunks   docqa/retrieval.py
 index.json  ---- load ------------------>  document blocks {citations: enabled}
   docqa/index.py                             |  (+ cache_control on the last one)
   (+ optional Voyage vectors)                v   docqa/qa.py
                                          Claude (Messages API)
                                              |
                                              v
                                    answer text + [1][2] markers
                                    Sources: title, location, cited_text
```

If retrieval finds nothing, the app answers "not in the documents" locally and makes no API call.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then put your ANTHROPIC_API_KEY in .env
pip install pypdf               # optional: PDF ingestion
pip install voyageai            # optional: embeddings retriever
```

## Run it

```bash
python main.py ingest data/                       # builds index.json
python main.py search "how long is the warranty"  # offline: shows retrieved chunks
python main.py ask "How long do I have to return an item?"
python main.py ask "Do you ship to Brazil?" --dry-run   # retrieval only, no API call
python main.py chat                               # interactive; follow-ups reuse cached docs
```

Expected shape of `ask` output (text will vary):

```
Items can be returned within 30 days of delivery for a full refund.[1]

Sources:
  [1] refund_policy.md [chars 0-474]  (chars 66-170)
      "Customers may return most items within 30 days of delivery for a full refund..."

usage: 1 request(s), in=1234 out=67 cache_read=0 cache_write=0 | ~$0.0031 (estimate)
```

A question the documents cannot answer ("What is the CEO's salary?") yields: `The provided documents do not contain the answer to this question.`

Useful options: `-k/--top-k`, `--model`, `--max-tokens`, `--no-cache`, `--dry-run`, `--retriever bm25|voyage|auto`, and for `ingest`: `--chunk-size`, `--overlap`, `--embed`. Run `python main.py <command> --help`.

## Claude features demonstrated

| Feature | Where | Course lesson |
|---|---|---|
| Document content blocks (`source.type: "text"`) | `docqa/qa.py` `document_block` | [2.7 PDF support](../../modules/module2_core_api/07_pdf_support.md), [2.8 Document analysis](../../modules/module2_core_api/08_document_analysis.md) |
| Citations (`citations: {"enabled": true}`; `cited_text`, `document_index`, char locations) | `document_block`, `build_answer` | [2.8](../../modules/module2_core_api/08_document_analysis.md), [Platform docs: citations](https://platform.claude.com/docs/en/build-with-claude/citations) |
| Prompt caching (`cache_control` on the document prefix, follow-ups in `chat`) | `QASession.build_messages` | [3.5 Prompt caching](../../modules/module3_advanced_features/05_prompt_caching.md) |
| System prompt that forces grounded answers and "not in the documents" | `SYSTEM_PROMPT` | [2.2 System prompts](../../modules/module2_core_api/02_system_prompts.md) |
| RAG: chunk, index, retrieve, generate | all of `docqa/` | [4.9 RAG fundamentals](../../modules/module4_applications/09_rag_fundamentals.md), [4.11 Embeddings](../../modules/module4_applications/11_embeddings.md), [4.2 Q&A systems](../../modules/module4_applications/02_qa_systems.md) |
| Usage and cost tracking, stop-reason handling (`refusal`, `max_tokens`, `pause_turn`) | `docqa/usage.py`, `build_answer` | [1.3 Pricing](../../modules/module1_foundation/03_pricing_limits.md) |
| Testing with a fake client | `tests/` | [4.20 Testing](../../modules/module4_applications/20_testing.md) |

All sources are listed in [REFERENCES.md](../../REFERENCES.md).

## Retrieval: BM25 by default, Voyage optionally

**Anthropic has no embeddings API.** Claude does not produce embeddings. The default retriever is therefore BM25, a keyword-ranking algorithm implemented in about 40 lines of pure Python (`BM25Retriever`): no services, no keys. Its weakness is vocabulary mismatch ("car" will not match "automobile").

For semantic search, Anthropic's docs point to Voyage AI, a separate provider with its own key:

```bash
export VOYAGE_API_KEY=...        # or in .env
pip install voyageai
python main.py ingest data/ --embed          # stores voyage-3.5 vectors in index.json
python main.py ask "..." --retriever voyage  # or --retriever auto (falls back to BM25)
```

Embedding calls send your chunk text to Voyage AI. Vectors are stored as JSON lists and compared with plain-Python cosine similarity, which is fine for small corpora only.

## How citations work here

Each retrieved chunk becomes its own `document` block titled `file [location]`. Claude's text blocks come back with a `citations` list; `document_index` says which block was cited and `start_char_index`/`end_char_index` are offsets inside that chunk. The app adds the chunk's own start offset so the printed location is a character range in the original file (or, for PDFs, in the page; the page number is shown too). The same quote is numbered once, however many times it is cited.

Rules worth remembering: citations must be enabled on all documents or none, and **citations cannot be combined with `output_config.format` (structured outputs)**; the API returns a 400, so this app never sets it. Cited text does not count toward output tokens.

## Prompt caching in `chat`

Each turn's user message is `[new document blocks..., question]`. Documents retrieved in earlier turns stay exactly where they were, and a follow-up only appends chunks it has not seen, so the conversation prefix is byte-identical and the cache can hit. The last document block of each turn carries `cache_control: {"type": "ephemeral"}` (the most recent 3 such turns are marked; the API allows 4 breakpoints). After 24 distinct chunks the session resets its document set to keep context bounded.

Honest limits: a prefix shorter than the model's minimum cacheable length (model-dependent, roughly 1,000 to 4,000 tokens) is silently not cached, and the 3 sample documents are far below that. Caching only shows up (`cache_read > 0` in the usage line) with larger documents. The default cache lifetime is 5 minutes.

## Configuration

| Setting | Default | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | none | required for `ask`/`chat`; never printed |
| `VOYAGE_API_KEY` | none | only for `--embed` / `--retriever voyage` |
| `--model` | `claude-sonnet-5-5` | any model that supports citations; `claude-haiku-4-5` is cheaper |
| `--chunk-size` / `--overlap` | 500 / 100 chars | smaller chunks give tighter citations |
| `-k/--top-k` | 4 | chunks sent per question |
| `PRICES` in `docqa/usage.py` | Sonnet 5.5 $2/$10, Haiku 4.5 $1/$5, Opus 5.5 $4/$20 per MTok | cache reads counted at 10%, writes at 1.25x; an estimate, check the pricing page |

No sampling parameters (`temperature` etc.) or prefill are used; current models reject them.

## Security notes

- Documents are untrusted input. The system prompt tells Claude to treat document text as data, but prompt injection through documents is not fully preventable; do not give this app tools that act on answers.
- The key is read from the environment or `.env` (git-ignored) and never printed. Model output is only printed, never executed.
- `ingest` reads only the paths you pass. Chunk text (not whole files) is what leaves your machine, to Anthropic and, with `--embed`, to Voyage AI.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

27 offline tests use a fake client (`tests/conftest.py`) that records requests and returns SDK-shaped responses. They cover chunking, BM25 ranking, citation rendering, index save/load, the "answer is not in the documents" paths, refusal and `max_tokens`, chat prefix stability and cache marks, usage and cost, the Voyage retriever (injected embedder), and the CLI.

## Limits and not verified live

- No live API call was made while building this; request and response shapes were checked against the installed `anthropic` SDK types and the course notes, not against the live service.
- Real PDF text extraction was not exercised in tests (the page-to-chunk logic is tested with a stubbed reader). PDFs are chunked as extracted text, so scanned PDFs, tables and layouts do not work, and Claude's native PDF mode (page-level citations) is not used.
- BM25 uses a crude plural stemmer and English stopwords. The JSON index is loaded fully into memory.
- Retrieval quality bounds answer quality: if the right chunk is not in the top-k, Claude will say the documents do not contain the answer.
- Chat history keeps answer text only (not citation blocks), and the Anthropic refusal fallback options are not used.

## Extend it

- Add a reranking step (retrieve 20, let Claude Haiku 4.5 pick the best 4).
- Hybrid retrieval: merge BM25 and Voyage rankings (reciprocal rank fusion).
- Send PDFs natively as base64 `document` blocks to get page-level citations.
- Stream answers with `client.messages.stream`.
- Swap the JSON index for a vector database ([4.10](../../modules/module4_applications/10_vector_databases.md)).
- Track file hashes for incremental ingest so unchanged files are not re-embedded.
