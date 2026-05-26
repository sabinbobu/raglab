# AGENTS.md

## Project Overview

RAGLab is a FastAPI-based RAG (Retrieval-Augmented Generation) evaluation platform. It runs a matrix of LLMs × prompt versions × retrieval strategies on a question corpus, then scores each combination with Ragas faithfulness, cost, and latency scorecards.

The goal: answer "which combination of LLM, retriever, and prompt performs best?"

See `pyproject.toml` for the Python version and all dependencies. The project uses `uv` for dependency management — not pip.

## Repository Structure

```
RAGLab/
├── src/raglab/
│   ├── main.py               # FastAPI app — all HTTP endpoints
│   ├── config.py             # Settings (pydantic-settings, .env) + MODEL_PRICING table
│   ├── cli.py                # Typer CLI — `raglab ingest <path>`
│   ├── telemetry.py          # Logfire setup for FastAPI
│   ├── gateway/              # LLM abstraction layer
│   │   ├── base.py           # LLMProvider Protocol + LLMResponse Pydantic model
│   │   ├── openai.py         # OpenAIProvider
│   │   ├── anthropic.py      # AnthropicProvider
│   │   └── factory.py        # get_provider(name) → LLMProvider
│   ├── retrieval/            # Retrieval strategies
│   │   ├── base.py           # Retriever Protocol + RetrievedChunk Pydantic model
│   │   ├── chroma.py         # ChromaRetriever (dense vector search)
│   │   ├── bm25.py           # BM25Retriever (sparse keyword search)
│   │   ├── hybrid.py         # HybridRetriever (Reciprocal Rank Fusion)
│   │   └── factory.py        # get_retriever(name, collection) → Retriever
│   ├── ingestion/            # Document ingestion pipeline
│   │   ├── loaders.py        # load_pdf, load_markdown → list[dict]
│   │   ├── chunkers.py       # recursive_chunk(text) → list[str]
│   │   └── embedder.py       # embed_batch(texts) → list[list[float]]
│   ├── experiments/          # Experiment runner and evaluation
│   │   ├── models.py         # RunResult SQLModel table
│   │   ├── runner.py         # ExperimentConfig + run_experiment()
│   │   └── eval.py           # evaluate_experiment() → list[Scorecard]
│   └── prompts/              # Versioned YAML prompt templates
│       ├── rag_v1.yaml       # Precise, citation-focused system prompt
│       └── rag_v2.yaml       # Conversational variant
├── tests/                    # pytest suite (all network calls mocked)
├── data/                     # Corpus directory (contents gitignored)
├── Dockerfile                # Multi-stage build: builder + runtime
├── docker-compose.yml        # Volumes for .chroma and raglab.db
├── pyproject.toml            # Dependencies, ruff/mypy/pytest config
└── uv.lock                   # Lockfile — always commit this
```

## Tech Stack

- **Python**: see `requires-python` in `pyproject.toml`
- **Web framework**: FastAPI + Pydantic v2 + Uvicorn
- **LLMs**: OpenAI (`openai` SDK) + Anthropic (`anthropic` SDK)
- **Vector DB**: ChromaDB (persistent local store at `.chroma/`)
- **Sparse retrieval**: `rank-bm25` (BM25Okapi)
- **ORM / database**: SQLModel + SQLite (`raglab.db`)
- **Evaluation**: Ragas (`Faithfulness` metric — LLM-as-judge via OpenAI)
- **Observability**: Logfire (optional; falls back to console logging if no token)
- **CLI**: Typer (`raglab ingest <path>`)
- **Dependency manager**: uv — use `uv sync`, not `pip install`
- **Linting**: ruff (E, F, I rules) + mypy (strict)
- **Tests**: pytest + pytest-mock

## Build & Run

```bash
# Install all dependencies (including dev group)
uv sync --group dev

# Copy and populate environment variables
cp .env.example .env
# Edit .env — set OPENAI_API_KEY and ANTHROPIC_API_KEY

# Ingest a corpus of PDFs or Markdown files
uv run raglab ingest data/sample/

# Start the API server (hot reload)
uv run uvicorn raglab.main:app --reload

# Or via Docker
docker compose up
```

Required environment variables (see `.env.example`):
- `OPENAI_API_KEY` — required for LLM calls and Ragas eval
- `ANTHROPIC_API_KEY` — required for Anthropic model calls
- `LOGFIRE_TOKEN` — optional; enables Logfire cloud tracing

## Testing

```bash
# Run all tests (zero real API calls — all network is mocked)
uv run pytest

# Lint + type check
uv run ruff check . && uv run mypy src

# Lint with auto-fix
uv run ruff check . --fix
```

Tests live in `tests/`. Every test that touches LLMs, ChromaDB, or the filesystem uses `unittest.mock.patch`. Never add tests that make real API calls — CI sets dummy keys.

## Key Patterns and Conventions

### Protocol-based interfaces

All LLM providers and retrievers satisfy Protocols defined in `base.py`. Never monkeypatch — implement the Protocol in a new class.

```python
# ✅ Correct: new class implementing the Protocol
class MyProvider:
    def generate(self, messages: list[dict[str, Any]], model: str) -> LLMResponse: ...

# ❌ Wrong: mutating an existing instance
existing_provider.generate = lambda ...: ...
```

### Adding a new LLM provider

1. Create `src/raglab/gateway/<name>.py` — implement `generate(messages, model) → LLMResponse`
2. Calculate cost using `MODEL_PRICING` from `src/raglab/config.py`
3. Wrap the SDK call in a Logfire span: `with logfire.span("<provider>.request", model=model):`
4. Register in `src/raglab/gateway/factory.py` → `get_provider()`
5. Add the new model's token pricing to `MODEL_PRICING` in `src/raglab/config.py`
6. Add mocked tests in `tests/test_gateway.py`

### Adding a new retriever

1. Create `src/raglab/retrieval/<name>.py` — implement `retrieve(query, top_k) → list[RetrievedChunk]`
2. Register in `src/raglab/retrieval/factory.py` → `get_retriever()`
3. Add mocked tests in `tests/test_retrieval.py`

### Adding a new prompt version

1. Create `src/raglab/prompts/rag_<version>.yaml`
2. Required keys: `version`, `system`, `user`
3. The `user` value must contain `{context}` and `{question}` placeholders
4. No code changes needed — `load_prompt(version)` resolves by filename and validates automatically

### Experiment matrix

`ExperimentConfig` in `src/raglab/experiments/runner.py` defines the cross-product:
- `models` × `prompt_versions` × `questions` = total runs
- All runs are persisted to `raglab.db` immediately after completion (crash-safe)
- **`provider` routes all models through one gateway** — if you pass `claude-*` model names, set `provider = "anthropic"`

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and PR to `main`:
1. `uv run ruff check .` — linting
2. `uv run mypy src` — type checking (strict)
3. `uv run pytest` — full test suite (dummy API keys injected via env)

Pre-commit hooks (`.pre-commit-config.yaml`): ruff auto-fix + format, trailing whitespace, EOF fixer, merge conflict detection, large file guard (1 MB).

## Common Pitfalls

- **Provider/model mismatch**: `ExperimentConfig.provider` routes all model names through a single provider. Mixing OpenAI and Anthropic model names in one config will fail — run separate experiments per provider.
- **ChromaDB path**: `.chroma/` is relative to CWD. The CLI, API server, and Docker container all expect to run from the repo root — otherwise the collection is not found.
- **`raglab.db` is append-only**: Running experiments does not overwrite previous runs. Query results by `experiment_id` to isolate a specific run set.
- **Ragas requires OpenAI**: `evaluate_experiment()` calls Ragas internally, which uses OpenAI as the judge LLM. `OPENAI_API_KEY` must be set even when evaluating Anthropic experiment runs.
- **`MODEL_PRICING` is manually maintained**: Update `src/raglab/config.py` whenever OpenAI or Anthropic changes pricing or you add new model names.
- **`data/` contents are gitignored**: Only `data/sample/.gitkeep` is tracked. Do not commit corpus PDFs or other large files.
