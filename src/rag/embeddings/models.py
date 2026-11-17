from dataclasses import dataclass


@dataclass(frozen=True)
class Embedding:
    text: str
    vector: list[float]
    model: str
    dimensions: int
