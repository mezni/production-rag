from rag.chunking.models import DocumentChunk


class ChunkValidator:

    @staticmethod
    def validate(
        chunks: list[DocumentChunk],
    ) -> None:

        if not chunks:
            raise ValueError("No chunks generated")

        for chunk in chunks:

            if not chunk.content.strip():
                raise ValueError("Empty chunk")

            if chunk.chunk_index < 0:
                raise ValueError("Invalid chunk index")

            if not chunk.document_id:
                raise ValueError("Missing document ID")
