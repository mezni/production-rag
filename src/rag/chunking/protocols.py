from typing import Protocol

from rag.chunking.models import DocumentChunk


class ChunkingStrategy(Protocol):
    def chunk(
        self,
        text: str,
        document_id: str,
    ) -> list[DocumentChunk]: ...
