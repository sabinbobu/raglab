# Copilot Instructions

## Python Conventions

- Python 3.12+. Use built-in generics (`list[str]`, `dict[str, Any]`) — no `from __future__ import annotations` needed.
- All public functions and methods must have type hints and a docstring.
- Use `pydantic.BaseModel` for all data transfer objects. Apply `ConfigDict(frozen=True)` to value objects (`LLMResponse`, `RetrievedChunk`).
- Import the `settings` singleton from `raglab.config` — never instantiate `Settings()` elsewhere.
- No secrets in source code. All credentials are loaded via `config.Settings` from `.env`.

## FastAPI Patterns

- Endpoint functions are synchronous (`def`, not `async def`) unless genuine async I/O is needed.
- Request bodies are Pydantic `BaseModel` subclasses — validate at the HTTP boundary, not inside service logic.
- Use `HTTPException` for expected failures (e.g., 404 when no chunks retrieved). Let unhandled exceptions surface as 500.
- The declared `response_model` must match the function's return type exactly.

## Protocol Implementation

- `LLMProvider` Protocol is in `src/raglab/gateway/base.py`: `generate(messages, model) → LLMResponse`
- `Retriever` Protocol is in `src/raglab/retrieval/base.py`: `retrieve(query, top_k) → list[RetrievedChunk]`
- New providers and retrievers implement the Protocol in a new class. Never monkeypatch.
- `get_provider()` and `get_retriever()` in their respective `factory.py` files are the only places that resolve implementations by string name.

## Prompt Registry

- Prompts are versioned YAML files in `src/raglab/prompts/` named `rag_<version>.yaml`.
- Required keys: `version`, `system`, `user`. The `user` template must contain `{context}` and `{question}` placeholders.
- Load via `load_prompt(version)` — this validates keys and placeholders on load and raises `FileNotFoundError` or `ValueError` for invalid templates.

## Test Conventions

- All tests live in `tests/`. File naming: `test_<module>.py`.
- Mock all network calls. No real LLM, embedding, or ChromaDB API calls in tests.
- Patch at the import location (not the original module):
  - ✅ `patch("raglab.gateway.openai.OpenAI")`
  - ❌ `patch("openai.OpenAI")`
  - ✅ `patch("raglab.retrieval.chroma.chromadb.PersistentClient")`
  - ✅ `patch("raglab.retrieval.chroma.embed_batch")`
- Shared fixtures go in `tests/conftest.py` (e.g., `fake_llm_response`).
- Run tests: `uv run pytest`

## Code Style

- Ruff (line length 88, E + F + I rules). Run: `uv run ruff check . --fix`
- mypy strict mode. All public APIs must be fully typed. Minimize `# type: ignore` — only acceptable at third-party SDK boundaries where types are missing.
- No LangChain, LlamaIndex, or other RAG frameworks — the pipeline is built from scratch.

## Observability

- Wrap LLM and retrieval calls in Logfire spans: `with logfire.span("service.operation", **kwargs):`
- Logfire is optional — `send_to_logfire="if-token-present"` means it silently logs to console when `LOGFIRE_TOKEN` is unset.

## Maintenance Matrix

When you change a file, these other files also need updating:

| You change… | Also update… |
|---|---|
| New LLM provider (`gateway/<name>.py`) | `gateway/factory.py` (register name), `config.py` (`MODEL_PRICING`), `tests/test_gateway.py` (add mocked test) |
| New retriever (`retrieval/<name>.py`) | `retrieval/factory.py` (register name), `tests/test_retrieval.py` (add mocked test) |
| New prompt version (`prompts/rag_<v>.yaml`) | No code changes — verify by passing the version string to `/query` or an experiment |
| `LLMResponse` fields (`gateway/base.py`) | `gateway/openai.py`, `gateway/anthropic.py` (construction), `tests/conftest.py` (fixture), `tests/test_gateway.py` (assertions) |
| `RetrievedChunk` fields (`retrieval/base.py`) | `retrieval/chroma.py`, `retrieval/bm25.py`, `retrieval/hybrid.py` (construction), `tests/test_retrieval.py` |
| `RunResult` fields (`experiments/models.py`) | `experiments/runner.py` (construction), `experiments/eval.py` (field access), SQLite schema migration if `raglab.db` already exists |
| Chunker signature (`ingestion/chunkers.py`) | `cli.py` (call site), `tests/test_ingestion.py` |
| Embedder signature (`ingestion/embedder.py`) | `retrieval/chroma.py` (call site), `cli.py` (call site), `tests/test_retrieval.py` (mock target) |
| `Settings` fields (`config.py`) | `.env.example` (document new variable), any test that mocks env |
| API endpoint added/changed (`main.py`) | `README.md` (API endpoints table), `tests/` (add or update endpoint test) |
| Token pricing (`MODEL_PRICING` in `config.py`) | `README.md` eval results table if documented numbers are affected |
