from uuid import uuid4

import pytest

from rag.embeddings.models import Embedding
from rag.retrieval.service import RetrievalService


class FakeEmbeddingService:
    def __init__(self):
        self.calls = []

    def embed(self, text: str) -> Embedding:
        self.calls.append(text)
        return Embedding(
            text=text,
            vector=[0.1, 0.2, 0.3],
            model="test-model",
            dimensions=3,
        )


class FakeRepository:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def search(self, **kwargs):
        self.calls.append(kwargs)
        return self.results


@pytest.fixture
def result_data():
    return {
        "chunk_id": uuid4(),
        "document_id": uuid4(),
        "content": "Refund within 30 days",
        "filename": "policy.pdf",
        "distance": 0.2,
        "metadata": {"chunk_index": 4},
    }


@pytest.fixture
def services(result_data):
    embedding_service = FakeEmbeddingService()
    repository = FakeRepository([result_data])
    service = RetrievalService(embedding_service, repository)
    return service, embedding_service, repository


def test_search(services, result_data):
    service, embedding_service, repository = services

    response = service.search(
        "  What is  the refund policy? ",
        tenant_id="tenant-1",
        top_k=3,
    )

    assert embedding_service.calls == ["What is the refund policy?"]
    assert repository.calls == [
        {
            "query_embedding": [0.1, 0.2, 0.3],
            "limit": 3,
            "tenant_id": "tenant-1",
        }
    ]
    assert response.query == "What is the refund policy?"
    assert response.top_k == 3
    assert len(response.results) == 1
    assert response.results[0].chunk_id == result_data["chunk_id"]
    assert response.results[0].document_id == result_data["document_id"]
    assert response.results[0].content == result_data["content"]
    assert response.results[0].filename == result_data["filename"]
    assert response.results[0].distance == 0.2
    assert response.results[0].similarity == 0.8
    assert response.results[0].metadata == {"chunk_index": 4}


@pytest.mark.parametrize("query", ["", "   "])
def test_search_rejects_empty_query(services, query):
    service, embedding_service, repository = services

    with pytest.raises(ValueError):
        service.search(query, tenant_id="tenant-1")

    assert embedding_service.calls == []
    assert repository.calls == []


@pytest.mark.parametrize("top_k", [0, -1, 101])
def test_search_rejects_invalid_top_k(services, top_k):
    service, embedding_service, repository = services

    with pytest.raises(ValueError):
        service.search("refund policy", tenant_id="tenant-1", top_k=top_k)

    assert embedding_service.calls == []
    assert repository.calls == []


def test_search_requires_tenant(services):
    service, embedding_service, repository = services

    with pytest.raises(ValueError):
        service.search("refund policy", tenant_id="")

    assert embedding_service.calls == []
    assert repository.calls == []
