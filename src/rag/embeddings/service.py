from rag.embeddings.models import Embedding
from rag.embeddings.protocols import EmbeddingProvider
from rag.embeddings.validator import EmbeddingValidator


class EmbeddingService:
    def __init__(
        self,
        provider: EmbeddingProvider,
        model: str,
        dimensions: int,
    ):
        self.provider = provider
        self.model = model
        self.dimensions = dimensions

    def embed(self, text: str) -> Embedding:

        if not text.strip():
            raise ValueError("Text cannot be empty")

        vector = self.provider.embed(text)

        EmbeddingValidator.validate(
            vector,
            self.dimensions,
        )

        return Embedding(
            text=text,
            vector=vector,
            model=self.model,
            dimensions=self.dimensions,
        )

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[Embedding]:

        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("Empty text in batch")

        vectors = self.provider.embed_batch(texts)

        if len(vectors) != len(texts):
            raise ValueError("Embedding count mismatch")

        results = []

        for text, vector in zip(texts, vectors):
            EmbeddingValidator.validate(
                vector,
                self.dimensions,
            )

            results.append(
                Embedding(
                    text=text,
                    vector=vector,
                    model=self.model,
                    dimensions=self.dimensions,
                )
            )

        return results
