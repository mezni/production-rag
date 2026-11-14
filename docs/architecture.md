# Architecture

## Overview

The project is organized in layers so that ingestion, domain models, and
chunking can evolve independently. Each layer depends only on the layers below
it.

```text
main.py
  └── ingestion/service.py
        ├── ingestion/validator.py
        ├── ingestion/parser.py
        ├── ingestion/normalizer.py
        └── ingestion/metadata.py

chunking/service.py
  ├── chunking/config.py
  ├── chunking/recursive.py
  └── models/{document,chunk}.py
```

## Components

### Domain models (`src/rag/models`)

- `Document` - normalized document content plus identity and metadata.
- `Chunk` - a slice of a document with `chunk_index`, `start_char`, and
  `end_char` offsets.

Both are dataclasses and carry a free-form `metadata` dictionary.

### Ingestion (`src/rag/ingestion`)

- `DocumentValidator` - rejects missing files, unsupported extensions, files
  over the size limit, and empty files.
- `ParserFactory` / `DocumentParser` - selects a parser by extension. Parsers:
  - `PDFParser` (pypdf)
  - `DOCXParser` (python-docx)
  - `TXTParser`
- `TextNormalizer` - removes control characters, normalizes line endings and
  whitespace, and collapses excess blank lines.
- `MetadataExtractor` - derives `source_path`, `document_type`, `extension`, and
  `file_size_bytes`. Document type is inferred from filename keywords
  (`contract`, `policy`, `procedure`).
- `DocumentIngestionService` - orchestrates validation, parsing, normalization,
  metadata extraction, and construction of a `Document`.

### Chunking (`src/rag/chunking`)

- `ChunkingConfig` - validated, immutable settings for chunk size, overlap, and
  boundary ratio.
- `RecursiveCharacterSplitter` - splits text using separators
  `["\n\n", "\n", ". ", " ", ""]`, preferring the largest natural boundary that
  fits within the configured chunk size.
- `ChunkingService` - converts a `Document` into `Chunk` objects, assigns UUIDs
  and sequential indices, and copies document metadata onto each chunk.

## Data flow

```text
file path
  -> validate
  -> parse to raw text
  -> normalize
  -> extract metadata
  -> Document
  -> split into segments (content, start, end)
  -> Chunk[]
```

## Design decisions

- **Protocol-based parsers.** `DocumentParser` is a `Protocol`, and the factory
  maps extensions to parser classes, making new formats easy to add.
- **Offset-preserving chunks.** Chunk content always equals
  `document.content[start_char:end_char]`, which supports traceability back to
  the source text.
- **Validated configuration.** `ChunkingConfig` fails fast on invalid values
  such as overlap greater than or equal to chunk size.
- **Dependency injection.** Services accept their collaborators or config via
  the constructor, keeping them testable.

## Extension points

- Add a parser by implementing `parse()` and registering the extension in
  `ParserFactory`.
- Replace the splitter by conforming to the same `split()` contract used by
  `ChunkingService`.
- Add embedding, indexing, retrieval, or generation as new packages that consume
  `Chunk` objects.
