# 4.3 RAG Optimization

Basic RAG often fails ("I can't find that info"). Optimization fixes this.

## 1. Hybrid Search
Combine **Keyword Search** (BM25) with **Semantic Search** (Embeddings).
- Keywords catch exact matches ("Error 503").
- Semantic catches concepts ("Server failure").

## 2. Reranking
1. Retrieve top 50 results (fast).
2. Use a **Reranker** model (Cohere Rerank) to sort them by relevance to the query.
3. Pass top 5 to Claude.

## 3. Query Expansion
Ask Claude to generate synonyms or sub-questions.
- User: "Compare X and Y."
- Agent: "Searching for X", "Searching for Y".

## 4. Contextual Retrieval
Instead of embedding just a raw chunk, ask Claude to add context *before* embedding.
- **Chunk:** "It was 50 dollars." (Ambiguous)
- **Enriched Chunk:** "The price of the Widget X mentioned in the 2024 report was 50 dollars." (Embed this).

## Next Steps
- Introduction to [MCP](./13_mcp_intro.md).
