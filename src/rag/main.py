from pathlib import Path

from rag.chunking.config import ChunkingConfig
from rag.chunking.service import ChunkingService
from rag.ingestion.service import DocumentIngestionService


def main() -> None:
    file_path = Path("data/contracts/contract-4821.pdf")

    ingestion_service = DocumentIngestionService()
    document = ingestion_service.ingest(file_path)

    chunking_service = ChunkingService(
        ChunkingConfig(
            chunk_size=1000,
            chunk_overlap=150,
        )
    )

    chunks = chunking_service.chunk_document(document)

    print(f"Document: {document.filename}")
    print(f"Document ID: {document.document_id}")
    print(f"Total characters: {len(document.content)}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "=" * 60)
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Character offsets: {chunk.start_char}:{chunk.end_char}")
        print(chunk.content)


if __name__ == "__main__":
    main()
