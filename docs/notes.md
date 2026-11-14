# Development Notes

## Commands

```bash
uv sync                  # install dependencies
uv run python -m rag.main  # run the ingestion example
uv run pytest            # run tests
uv run ruff check .      # lint
uv run ruff format .     # format
```

## Conventions

- Python 3.12+, type hints on public functions and methods.
- One responsibility per module; services orchestrate, helpers stay small.
- Domain objects are dataclasses with a free-form `metadata` dict.
- Configuration is validated at construction time.
- Dependencies are added with `uv add` so `pyproject.toml` and `uv.lock` stay in
  sync.

## Sample data

`data/` contains generated sample documents used by the example and tests:

```text
data/contracts/contract-4821.pdf
data/contracts/contract-4822.pdf
data/policies/return-policy.docx
data/policies/security-policy.pdf
data/procedures/refund-procedure.txt
```

## Testing notes

- Test files are split by concern under `tests/ingestion/` and `tests/chunking/`.
- `pytest` currently reports an import mismatch because two test modules share
  the basename `test_service.py` and the test directories are not packages.
  Add `__init__.py` files under `tests/` (or rename one module) to resolve it:

  ```bash
  touch tests/__init__.py tests/ingestion/__init__.py tests/chunking/__init__.py
  ```

## Known limitations

- Metadata `document_type` is inferred from filenames, not file contents.
- Only local files are supported; there is no remote/object-storage source yet.
- Chunking splits on characters, not tokens.
- No embedding, retrieval, or generation stage is implemented yet.

## Future work

- Token-aware chunking and configurable separators.
- Idempotent document and chunk identifiers for incremental indexing.
- Embedding provider abstraction and a vector store adapter.
- Retrieval with metadata filters and reranking.
- Evaluation harness for retrieval and answer quality.
