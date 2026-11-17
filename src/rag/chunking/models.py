from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: dict
