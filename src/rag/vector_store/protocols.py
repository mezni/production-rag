from typing import Protocol
from uuid import UUID


class VectorRepository(Protocol):
    def save(
        self,
        chunk_id: UUID,
        embedding: list[float],
        model_name: str,
    ) -> None: ...

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
        tenant_id: str | None = None,
    ) -> list[dict]: ...
