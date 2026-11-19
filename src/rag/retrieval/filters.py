from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalFilters:
    tenant_id: str
    department: str | None = None
    document_type: str | None = None
