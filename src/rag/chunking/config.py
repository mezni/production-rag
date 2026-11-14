from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkingConfig:
    chunk_size: int = 1000
    chunk_overlap: int = 150
    min_boundary_ratio: float = 0.5

    def __post_init__(self) -> None:
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        if not 0 < self.min_boundary_ratio <= 1:
            raise ValueError("min_boundary_ratio must be between 0 and 1")
