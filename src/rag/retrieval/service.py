from rag.retrieval.models import (
    RetrievalResponse,
    RetrievalResult,
)
from rag.retrieval.query_preprocessor import QueryPreprocessor
from rag.retrieval.query_validator import QueryValidator


class RetrievalService:
    def __init__(
        self,
        embedding_service,
        repository,
    ):
        self.embedding_service = embedding_service
        self.repository = repository

    def search(
        self,
        query: str,
        tenant_id: str,
        top_k: int = 5,
    ) -> RetrievalResponse:

        QueryValidator.validate(query)

        if top_k <= 0 or top_k > 100:
            raise ValueError("Invalid top_k")

        if not tenant_id:
            raise ValueError("Tenant ID is required")

        processed_query = QueryPreprocessor.process(query)

        query_embedding = self.embedding_service.embed(processed_query)

        results = self.repository.search(
            query_embedding=query_embedding.vector,
            limit=top_k,
            tenant_id=tenant_id,
        )

        retrieval_results = [
            RetrievalResult(
                chunk_id=result["chunk_id"],
                document_id=result["document_id"],
                content=result["content"],
                filename=result["filename"],
                distance=float(result["distance"]),
                metadata=result["metadata"],
            )
            for result in results
        ]

        return RetrievalResponse(
            query=processed_query,
            results=retrieval_results,
            top_k=top_k,
        )
