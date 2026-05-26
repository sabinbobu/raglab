## What does this PR do?

<!-- One paragraph. What problem does it solve, and how? -->

## Changes

<!-- List the key files changed and what was done in each. -->

- `src/raglab/...` —
- `tests/...` —

## How to test

```bash
uv run pytest
uv run ruff check . && uv run mypy src
```

<!-- If you added a new provider, retriever, or endpoint — include a curl/pytest snippet showing it works. -->

## Checklist

- [ ] Tests added or updated for every changed behaviour
- [ ] `uv run pytest` passes locally
- [ ] `uv run ruff check . && uv run mypy src` passes with no new errors
- [ ] If adding a new LLM provider: `gateway/factory.py` and `config.py` (`MODEL_PRICING`) updated
- [ ] If adding a new retriever: `retrieval/factory.py` updated
- [ ] If adding a new prompt version: YAML validated (keys: `version`, `system`, `user`; placeholders: `{context}`, `{question}`)
- [ ] If changing `LLMResponse` or `RetrievedChunk` fields: all construction sites and `tests/conftest.py` updated
- [ ] If changing a public API endpoint: `README.md` endpoints table updated
- [ ] No secrets committed — credentials via `.env` only
