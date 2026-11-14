# production-rag

A small, production-oriented RAG (Retrieval-Augmented Generation) pipeline in
Python. The current implementation covers document ingestion and chunking, with
retrieval and generation planned as the next stages.

## Features

- Document validation (existence, file type, size limits).
- PDF, DOCX, and TXT parsing behind a `ParserFactory`.
- Text normalization (control characters, line endings, whitespace).
- Metadata extraction (source path, document type, extension, file size).
- Standard `Document` and `Chunk` domain models.
- Recursive character chunking with configurable size, overlap, and boundary
  strategy.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Usage

Run the ingestion example:

```bash
uv run python -m rag.main
```

Ingest and chunk a document programmatically:

```python
from pathlib import Path

from rag.chunking import ChunkingConfig, ChunkingService
from rag.ingestion.service import DocumentIngestionService

document = DocumentIngestionService().ingest(
    Path("data/contracts/contract-4821.pdf")
)

chunks = ChunkingService(ChunkingConfig()).chunk_document(document)

for chunk in chunks:
    print(chunk.chunk_index, chunk.start_char, chunk.end_char)
```

## Project layout

```text
data/                    Sample documents (contracts, policies, procedures)
docs/                    Architecture, lifecycle, and development notes
src/rag/
  main.py                Ingestion example entry point
  ingestion/             Validation, parsing, normalization, metadata
  models/                Document and Chunk domain models
  chunking/              Chunking configuration, splitter, and service
tests/                   Ingestion and chunking unit tests
```

## Testing

```bash
uv run pytest
```

## Linting

```bash
uv run ruff check .
```

## Documentation

- [docs/architecture.md](docs/architecture.md) - components and data flow
- [docs/rag-lifecycle.md](docs/rag-lifecycle.md) - end-to-end RAG stages
- [docs/notes.md](docs/notes.md) - development notes and conventions
