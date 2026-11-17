from rag.chunking.service import ChunkingService
from rag.chunking.strategies.fixed_size import FixedSizeChunker
from rag.models.document import Document


def test_process_chunks_document_with_strategy():
    document = Document(
        document_id="doc-4821",
        filename="contract-4821.txt",
        file_type=".txt",
        content="Termination clause. " * 30,
        metadata={"source_path": "data/contracts/contract-4821.txt"},
    )

    service = ChunkingService(
        FixedSizeChunker(chunk_size=100, overlap=20),
    )

    chunks = service.process(document.content, document.document_id)

    assert len(chunks) > 1
    assert all(chunk.document_id == "doc-4821" for chunk in chunks)
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert all(chunk.content.strip() for chunk in chunks)
