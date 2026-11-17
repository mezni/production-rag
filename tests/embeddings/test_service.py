import pytest

from rag.embeddings.service import EmbeddingService


class FakeEmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


def test_embed_text():

    service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
        model="test-model",
        dimensions=3,
    )

    result = service.embed("Refund policy")

    assert result.text == "Refund policy"
    assert len(result.vector) == 3
    assert result.model == "test-model"


def test_embed_empty_text():

    service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
        model="test-model",
        dimensions=3,
    )

    with pytest.raises(ValueError):
        service.embed("")


def test_embed_batch():

    service = EmbeddingService(
        provider=FakeEmbeddingProvider(),
        model="test-model",
        dimensions=3,
    )

    results = service.embed_batch(
        [
            "Refund policy",
            "Shipping policy",
        ]
    )

    assert len(results) == 2
