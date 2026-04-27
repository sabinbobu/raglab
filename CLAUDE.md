# RAGLab — Claude Code Instructions

## Project
FastAPI-based RAG evaluation platform. Compares LLMs × prompts × retrievers
on a corpus (sample), outputs scorecards with faithfulness/cost/latency.

## Stack
- Python 3.12, uv for deps, FastAPI, Pydantic v2
- LLMs: OpenAI + Anthropic (both via native SDKs, wrapped behind LLMProvider protocol)
- Vector DB: ChromaDB (pgvector adapter later)
- Eval: Ragas + custom cost/latency metrics
- Tests: pytest, mocked LLM calls

## Conventions
- All LLM/retriever/embedder interfaces are Protocols in `base.py` — new providers implement, never monkeypatch.
- Prompts live in YAML under `src/raglab/prompts/`, loaded by version string.
- No secrets in code. Everything via `config.Settings`.
- Every public function: type hints + docstring.
- Tests mock network calls — no real API hits in CI.

## Don't
- Don't add LangChain or LlamaIndex. We build the pipeline ourselves.
- Don't introduce async unless the endpoint actually benefits.
- Don't commit `data/` contents or `.env`.

## Commands
- `uv run pytest` — tests
- `uv run ruff check . && uv run mypy src` — lint + types
- `uv run raglab ingest data/bmw/` — ingestion CLI
- `uv run uvicorn raglab.main:app --reload` — dev server
