from uuid import uuid4

from rag.chunking.config import ChunkingConfig
from rag.chunking.recursive import RecursiveCharacterSplitter
from rag.models.chunk import Chunk
from rag.models.document import Document


class ChunkingService:
    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config

        self.splitter = RecursiveCharacterSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            min_boundary_ratio=config.min_boundary_ratio,
        )

    def chunk_document(self, document: Document) -> list[Chunk]:
        segments = self.splitter.split(document.content)

        chunks = []

        for index, (content, start, end) in enumerate(segments):
            chunk = Chunk(
                chunk_id=str(uuid4()),
                document_id=document.document_id,
                chunk_index=index,
                content=content,
                start_char=start,
                end_char=end,
                metadata={
                    **document.metadata,
                    "filename": document.filename,
                    "file_type": document.file_type,
                },
            )

            chunks.append(chunk)

        return chunks
