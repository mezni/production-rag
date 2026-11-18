CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id UUID PRIMARY KEY,
    filename VARCHAR(500) NOT NULL,
    content_hash VARCHAR(128) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documents_content_hash
ON documents(content_hash);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL
        REFERENCES documents(id)
        ON DELETE CASCADE,

    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    start_char INTEGER,
    end_char INTEGER,
    metadata JSONB NOT NULL DEFAULT '{}',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_document_chunk
        UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_document_chunks_document_id
ON document_chunks(document_id);

CREATE INDEX idx_document_chunks_metadata
ON document_chunks USING GIN(metadata);

CREATE TABLE chunk_embeddings (
    id UUID PRIMARY KEY,
    chunk_id UUID NOT NULL UNIQUE
        REFERENCES document_chunks(id)
        ON DELETE CASCADE,

    embedding VECTOR(1536) NOT NULL,
    model_name VARCHAR(150) NOT NULL,
    dimensions INTEGER NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_embedding_dimensions
        CHECK (dimensions = 1536)
);

CREATE INDEX idx_chunk_embeddings_hnsw
ON chunk_embeddings
USING HNSW (embedding vector_cosine_ops);
