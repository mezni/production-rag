from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    metadata: dict[str, Any] = field(default_factory=dict)
