# CHANGELOG — Production-Oriented RAG

All notable project development milestones, implementation decisions, engineering trade-offs, and progress are documented here.

---

# Day 1 — RAG Foundations and Architecture

**Status:** Completed

## Objective

Understand Retrieval-Augmented Generation (RAG), its architecture, lifecycle, and application in enterprise knowledge systems.

## Topics Covered

- RAG fundamentals.
- RAG versus fine-tuning.
- LLM limitations and hallucinations.
- Indexing pipeline.
- Query pipeline.
- Embeddings and vector similarity.
- Semantic search.
- Top-K retrieval.
- Context windows.
- Grounded generation.
- Retrieval precision and recall.
- Document storage versus vector storage.

## Architecture Designed

### Indexing Pipeline

```text
Documents
    |
    v
Document Loader
    |
    v
Parser
    |
    v
Text Normalizer
    |
    v
Chunking
    |
    v
Embedding
    |
    v
Vector Database
```

### Query Pipeline

```text
User Question
    |
    v
Query Processing
    |
    v
Query Embedding
    |
    v
Retrieval
    |
    v
Reranking
    |
    v
Context Builder
    |
    v
LLM Generation
    |
    v
Answer Validation
    |
    v
Answer with Citations
```

## Key Engineering Decisions

| Decision | Choice | Reason |
|---|---|---|
| Architecture | Two independent pipelines | Separate indexing from querying |
| Retrieval | Vector similarity search | Retrieve semantically relevant content |
| Storage | Document store + vector database | Separate source files from searchable vectors |
| Generation | Grounded LLM generation | Reduce unsupported answers |
| Framework | Plain Python initially | Understand core RAG concepts |

## Deliverables

- `docs/architecture.md`
- `docs/architecture.mmd`
- `docs/rag-lifecycle.md`
- `docs/day-01-notes.md`

## Key Learning

RAG is not simply an LLM connected to a vector database. It is an end-to-end information retrieval and generation system.

---

# Day 2 — Document Ingestion Engineering

**Status:** Implemented as learning baseline

## Objective

Build a document ingestion pipeline that validates source files, extracts content, normalizes text, and produces a standardized Document object.

## Problem Being Solved

Enterprise knowledge exists in multiple formats.

Before documents can be chunked, embedded, and indexed, they must be converted into a consistent representation.

## Components Implemented

| Component | Responsibility |
|---|---|
| Document Validator | Validate file existence, type, and size |
| Document Parser | Extract PDF, DOCX, and TXT content |
| Text Normalizer | Clean and normalize extracted text |
| Metadata Extractor | Extract file metadata |
| Document Model | Standardize document representation |
| Ingestion Service | Orchestrate the ingestion pipeline |

## Supported Formats

- PDF
- DOCX
- TXT

## Implementation

```text
src/rag/
├── models/
│   └── document.py
│
├── ingestion/
│   ├── validator.py
│   ├── parser.py
│   ├── normalizer.py
│   ├── metadata.py
│   └── service.py
│
└── main.py
```

## Domain Model

```python
@dataclass
class Document:
    document_id: str
    filename: str
    file_type: str
    content: str
    metadata: dict
```

## Dependencies

Production dependencies:

- `pypdf`
- `python-docx`

Development dependencies:

- `pytest`
- `ruff`

Package management:

- `uv`

## Key Engineering Decisions

| Decision | Choice | Reason |
|---|---|---|
| Supported formats | PDF, DOCX, TXT | Initial enterprise document types |
| Parsing | Format-specific parsers | Isolate extraction logic |
| Validation | Dedicated validator | Prevent invalid input |
| Normalization | Separate component | Keep extracted content consistent |
| Metadata | Separate extractor | Preserve source information |
| Orchestration | Ingestion service | Centralize pipeline execution |

## Testing

Initial tests cover:

- File validation.
- Unsupported file formats.
- Empty files.
- Text normalization.
- Control-character handling.

Additional tests required:

- Malformed PDF and DOCX files.
- Oversized files.
- Empty extracted content.
- Parser failures.
- Ingestion service failures.

## Production Improvements Identified

- OCR for scanned documents.
- PDF page-level provenance.
- DOCX table extraction.
- File content validation.
- Malware scanning.
- Content hashing and deduplication.
- Document versioning.
- Asynchronous ingestion.
- Retry and failure handling.
- Structured logging and observability.

## Key Learning

Document ingestion is a separate engineering responsibility. Downstream RAG components should consume standardized Document objects rather than handling individual file formats.

---

# Day 3 — Chunking Engineering

**Status:** Implemented as learning baseline

## Objective

Build a configurable chunking engine that transforms normalized documents into smaller, traceable units suitable for embedding and retrieval.

## Problem Being Solved

Large documents cannot be efficiently retrieved as a single unit.

For example, a 100-page contract may contain relevant information in several sections. Arbitrary splitting can separate conditions, exceptions, and important context.

The chunking engine must create manageable segments while preserving document relationships and provenance.

## Topics Covered

- Fixed-size chunking.
- Recursive character chunking.
- Sentence-based chunking.
- Semantic chunking.
- Chunk size.
- Chunk overlap.
- Character offsets.
- Document provenance.
- Metadata propagation.
- Chunking trade-offs.

## Components Implemented

| Component | Responsibility |
|---|---|
| Chunk Model | Represent a document segment |
| Chunking Config | Configure size, overlap, and boundary threshold |
| Recursive Splitter | Split content using text boundaries |
| Chunking Service | Orchestrate document-to-chunk transformation |

## Architecture

```text
Document
    |
    v
Chunking Service
    |
    v
Chunking Configuration
    |
    v
Recursive Character Splitter
    |
    v
Boundary Selection
    |
    v
Overlap Handling
    |
    v
Chunk Metadata
    |
    v
List of Chunks
```

## Initial Configuration

| Parameter | Value |
|---|---:|
| Chunk size | 1,000 characters |
| Chunk overlap | 150 characters |
| Minimum boundary ratio | 0.5 |
| Strategy | Recursive character |

These values are experimental starting points and require evaluation against real retrieval workloads.

## Domain Model

```python
@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    metadata: dict
```

## Implementation

```text
src/rag/
├── models/
│   ├── document.py
│   └── chunk.py
│
├── chunking/
│   ├── config.py
│   ├── recursive.py
│   └── service.py
│
└── ingestion/
    └── ...
```

## Key Engineering Decisions

| Decision | Choice | Reason |
|---|---|---|
| Chunk representation | Dedicated Chunk model | Preserve content and provenance |
| Initial strategy | Recursive character | General-purpose baseline |
| Configuration | Separate configuration object | Enable experimentation |
| Overlap | Configurable | Preserve boundary context |
| Offsets | Character positions | Support source traceability |
| Metadata | Propagate document metadata | Preserve source relationships |
| Service design | Separate from ingestion | Maintain separation of concerns |

## Testing

Tests cover:

- Empty text.
- Short text.
- Long text splitting.
- Original character offsets.
- Chunk overlap.
- Configuration validation.
- Document metadata preservation.
- Chunk ordering.

## Experiments

Three initial configurations:

| Experiment | Chunk size | Overlap |
|---|---:|---:|
| A | 500 | 50 |
| B | 1,000 | 150 |
| C | 1,500 | 300 |

Evaluation observations to record:

- Total chunk count.
- Average chunk length.
- Maximum chunk length.
- Overlap ratio.
- Preservation of meaningful sections.
- Retrieval quality once retrieval is implemented.

## Production Improvements Identified

- Token-aware chunking.
- Semantic chunking.
- Section-aware chunking.
- Table-aware chunking.
- Page-level provenance.
- Deterministic chunk identifiers.
- Document versioning.
- Chunking quality evaluation.
- Duplicate chunk detection.

## Key Learning

Chunking directly influences retrieval quality. The best strategy must be selected through evaluation rather than relying on arbitrary chunk-size defaults.

---

# Project Engineering Decisions

The following decisions apply across the project.

| Area | Decision |
|---|---|
| Project | `production-rag` |
| Language | Python |
| Package manager | uv |
| Architecture | Modular components |
| Initial implementation | Plain Python |
| API | FastAPI |
| LLM | OpenAI API |
| Embeddings | OpenAI embedding models |
| Vector database | PostgreSQL + pgvector |
| Testing | pytest |
| Linting | Ruff |
| Evaluation | Custom evaluation + RAGAS |
| Observability | OpenTelemetry + Langfuse |
| Containerization | Docker |
| Progress tracking | CHANGELOG.md |

## Engineering Principles

1. Separate business logic from infrastructure.
2. Keep components independently testable.
3. Preserve document and chunk provenance.
4. Use explicit configuration.
5. Validate inputs and outputs.
6. Handle failures explicitly.
7. Measure quality before optimizing.
8. Introduce frameworks only after understanding their underlying concepts.
9. Design for security and observability from the beginning.
10. Keep architecture documentation synchronized with implementation.

---

# Upcoming Milestones

| Day | Milestone | Main Deliverable | Status |
|---|---|---|---|
| 1 | RAG Foundations and Architecture | Architecture documentation | Completed |
| 2 | Document Ingestion | Ingestion pipeline | Implemented |
| 3 | Chunking Engineering | Chunking engine | Implemented |
| 4 | Embeddings Engineering | Embedding service | Planned |
| 5 | Vector Database Engineering | Vector repository | Planned |
| 6 | Retrieval Engineering | Retrieval service | Planned |
| 7 | Reranking Engineering | Reranking service | Planned |
| 8 | Generation Engineering | Generation service | Planned |
| 9 | Advanced RAG | Advanced retrieval strategies | Planned |
| 10 | RAG Evaluation | Evaluation framework | Planned |
| 11 | RAG Security | Security controls | Planned |
| 12 | RAG Observability | Observability integration | Planned |
| 13 | Performance Engineering | Performance benchmarks | Planned |
| 14 | Production Deployment | Deployable RAG application | Planned |
| 15 | Enterprise RAG | Enterprise architecture | Planned |

---

# Next Milestone — Day 4: Embeddings Engineering

## Objective

Transform document chunks into numerical vectors that represent their semantic meaning.

## Planned Components

- Embedding model interface.
- OpenAI embedding provider.
- Embedding service.
- Batch embedding processor.
- Vector dimension validation.
- Retry and error handling.
- Token usage and cost tracking.

## Expected Data Flow

```text
Document
    |
    v
Chunking Service
    |
    v
Chunks
    |
    v
Embedding Service
    |
    v
Embedding Provider
    |
    v
Numerical Vectors
    |
    v
Vector Database (Day 5)
```

## Expected Deliverables

- `src/rag/embeddings/`
- `src/rag/models/embedding.py`
- `tests/embeddings/`
- `docs/day-04-notes.md`
- Updated `docs/architecture.md`
- Updated `docs/architecture.mmd`

**Project status:** Three learning milestones completed. The next focus is Embeddings Engineering.


## Day 4 — Embeddings Engineering

### Added
- Embedding domain model.
- Embedding provider protocol.
- OpenAI embedding provider.
- Embedding service.
- Vector dimension validation.
- Single and batch embedding generation.
- Embedding service unit tests.
- Embedding engineering documentation.

### Architecture Decisions
- Introduced provider abstraction.
- Selected OpenAI text-embedding-3-small.
- Defined vector dimension configuration.
- Established embedding validation boundaries.
- Prepared the architecture for pgvector integration.

### Next
- Day 5 — Advanced Document Chunking Engineering.
