# RAG Lifecycle

This document describes the stages of the RAG pipeline as implemented in this
repository and the stages planned next.

## Implemented

| Stage | Component | Input | Output |
| --- | --- | --- | --- |
| 1. Validation | `DocumentValidator` | File path | Validated path or error |
| 2. Parsing | `PDFParser`, `DOCXParser`, `TXTParser` | File path | Raw text |
| 3. Normalization | `TextNormalizer` | Raw text | Clean text |
| 4. Metadata extraction | `MetadataExtractor` | File path | Metadata dict |
| 5. Document assembly | `DocumentIngestionService` | Validated, parsed, normalized data | `Document` |
| 6. Chunking | `ChunkingService` | `Document` | `Chunk[]` |

## Stage details

### 1. Validation

Checks that the file exists, is a regular file, has a supported extension
(`.pdf`, `.docx`, `.txt`), does not exceed the size limit (20 MB by default),
and is not empty.

### 2. Parsing

The `ParserFactory` selects a parser based on the file extension:

- PDF pages are read with `pypdf`, extracting text page by page.
- DOCX paragraphs are read with `python-docx`.
- TXT files are read as UTF-8 with replacement for invalid bytes.

### 3. Normalization

Removes control characters, converts `\r\n` and `\r` to `\n`, collapses runs of
spaces and tabs, reduces three or more consecutive newlines to a blank line, and
strips leading/trailing whitespace.

### 4. Metadata extraction

Produces `source_path`, `document_type`, `extension`, and `file_size_bytes`.
`document_type` is inferred from the filename (`contract`, `policy`,
`procedure`, or `unknown`).

### 5. Document assembly

Builds a `Document` with `document_id` (file stem), `filename`, `file_type`,
normalized `content`, and `metadata`.

### 6. Chunking

`RecursiveCharacterSplitter` walks the normalized text, choosing the largest
natural boundary that fits within `chunk_size`. Consecutive chunks overlap by
`chunk_overlap` characters, and each chunk records its `start_char`/`end_char`
offsets into the document content.

Default configuration:

```text
chunk_size         = 1000
chunk_overlap      = 150
min_boundary_ratio = 0.5
```

## Planned

The following stages are not implemented yet and define the roadmap:

| Stage | Purpose |
| --- | --- |
| Embedding | Convert chunks into vectors using an embedding model |
| Indexing | Persist vectors and metadata in a vector store |
| Retrieval | Retrieve relevant chunks for a query (optionally with reranking) |
| Generation | Build a grounded prompt and generate an answer with citations |
| Evaluation | Measure retrieval quality and answer faithfulness |

## End-to-end view

```text
documents -> ingest -> chunk -> embed -> index
                                          |
query ------------------------------------+
                                          |
                     retrieve -> rerank -> generate -> answer + citations
```
