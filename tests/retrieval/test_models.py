from uuid import uuid4

from rag.retrieval.models import RetrievalResponse, RetrievalResult


def test_result_similarity():
    result = RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        content="Refund policy",
        filename="policy.pdf",
        distance=0.25,
    )

    assert result.similarity == 0.75
    assert result.metadata == {}


def test_response_keeps_results_and_top_k():
    result = RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        content="Refund policy",
        filename="policy.pdf",
        distance=0.1,
        metadata={"source": "policy.pdf"},
    )

    response = RetrievalResponse(
        query="refund policy",
        results=[result],
        top_k=3,
    )

    assert response.query == "refund policy"
    assert response.results == [result]
    assert response.top_k == 3
