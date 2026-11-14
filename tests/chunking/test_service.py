from rag.chunking.config import ChunkingConfig
from rag.chunking.service import ChunkingService
from rag.models.document import Document


def test_chunk_document_preserves_document_metadata():
    document = Document(
        document_id="doc-4821",
        filename="contract-4821.txt",
        file_type=".txt",
        content="Termination clause. " * 30,
        metadata={"source_path": "data/contracts/contract-4821.txt"},
    )

    service = ChunkingService(ChunkingConfig(chunk_size=100, chunk_overlap=20))

    chunks = service.chunk_document(document)

    assert len(chunks) > 1
    assert all(chunk.document_id == "doc-4821" for chunk in chunks)
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert all(
        chunk.metadata["source_path"] == "data/contracts/contract-4821.txt"
        for chunk in chunks
    )
