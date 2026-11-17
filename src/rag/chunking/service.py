from rag.chunking.protocols import ChunkingStrategy
from rag.chunking.validator import ChunkValidator


class ChunkingService:

    def __init__(
        self,
        strategy: ChunkingStrategy,
    ):
        self.strategy = strategy

    def process(
        self,
        text: str,
        document_id: str,
    ):

        if not text.strip():
            raise ValueError("Document cannot be empty")

        chunks = self.strategy.chunk(
            text,
            document_id,
        )

        ChunkValidator.validate(chunks)

        return chunks
