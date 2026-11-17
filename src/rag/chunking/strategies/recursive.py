from uuid import uuid4

from rag.chunking.models import DocumentChunk


class RecursiveChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 100,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("Invalid overlap")

        self.chunk_size = chunk_size
        self.overlap = overlap

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ]

    def _split(
        self,
        text: str,
        separator_index: int = 0,
    ) -> list[str]:

        if len(text) <= self.chunk_size:
            return [text]

        separator = self.separators[separator_index]

        if not separator:
            return [
                text[i : i + self.chunk_size]
                for i in range(
                    0,
                    len(text),
                    self.chunk_size,
                )
            ]

        parts = text.split(separator)

        chunks = []
        current = ""

        for part in parts:
            candidate = current + separator + part if current else part

            if len(candidate) <= self.chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(current)

            if len(part) > self.chunk_size:
                chunks.extend(
                    self._split(
                        part,
                        separator_index + 1,
                    )
                )
                current = ""
            else:
                current = part

        if current:
            chunks.append(current)

        return chunks

    def chunk(
        self,
        text: str,
        document_id: str,
    ) -> list[DocumentChunk]:

        pieces = self._split(text)

        results = []

        for index, content in enumerate(pieces):
            results.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document_id,
                    content=content,
                    chunk_index=index,
                    start_char=0,
                    end_char=len(content),
                    metadata={},
                )
            )

        return results
