from typing import Protocol


class RetrievalRepository(Protocol):
    def search(
        self,
        query_embedding: list[float],
        limit: int,
        tenant_id: str,
    ) -> list[dict]: ...
