from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: UUID
    document_id: UUID
    content: str
    filename: str
    distance: float
    metadata: dict = field(default_factory=dict)

    @property
    def similarity(self) -> float:
        return 1.0 - self.distance


@dataclass(frozen=True)
class RetrievalResponse:
    query: str
    results: list[RetrievalResult]
    top_k: int
