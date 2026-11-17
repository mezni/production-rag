from uuid import uuid4

from rag.chunking.models import DocumentChunk


class FixedSizeChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("Invalid overlap")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
        document_id: str,
    ) -> list[DocumentChunk]:

        results = []
        start = 0
        index = 0
        step = self.chunk_size - self.overlap

        while start < len(text):
            end = min(
                start + self.chunk_size,
                len(text),
            )

            content = text[start:end]

            results.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document_id,
                    content=content,
                    chunk_index=index,
                    start_char=start,
                    end_char=end,
                    metadata={},
                )
            )

            start += step
            index += 1

        return results
