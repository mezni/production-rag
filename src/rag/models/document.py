from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Document:
    document_id: str
    filename: str
    file_type: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def source_path(self) -> Path | None:
        source = self.metadata.get("source_path")
        return Path(source) if source else None
