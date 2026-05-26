# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] — 2026-05-12

### Added

- **LLM Gateway** — `LLMProvider` Protocol, `LLMResponse` Pydantic model; `OpenAIProvider` and `AnthropicProvider` with token cost and latency tracking
- **Ingestion pipeline** — PDF and Markdown loaders, recursive chunker with overlap, OpenAI `text-embedding-3-small` batch embedder, ChromaDB persistent storage
- **Retrieval strategies** — `ChromaRetriever` (dense vector), `BM25Retriever` (sparse keyword), `HybridRetriever` (Reciprocal Rank Fusion)
- **Prompt registry** — versioned YAML templates (`rag_v1.yaml`, `rag_v2.yaml`) with validation on load
- **Experiment runner** — matrix of models × prompt versions × questions via `itertools.product`; crash-safe SQLite persistence per run
- **Evaluation harness** — Ragas `Faithfulness` metric; `Scorecard` with avg cost and latency per (model, prompt) combination
- **FastAPI endpoints** — `POST /generate`, `POST /query`, `POST /experiments/run`, `POST /experiments/evaluate`
- **CLI** — `raglab ingest <path>` via Typer
- **Observability** — Logfire tracing for FastAPI, OpenAI, Anthropic, and ChromaDB spans
- **Docker** — multi-stage `Dockerfile` + `docker-compose.yml` with volume mounts for `.chroma` and `raglab.db`
- **CI** — GitHub Actions: ruff + mypy + pytest on every push and PR to `main`
- **Pre-commit** — ruff auto-fix, trailing whitespace, EOF fixer, merge conflict check

[Unreleased]: https://github.com/sabinbobu/RAGLab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sabinbobu/RAGLab/releases/tag/v0.1.0
