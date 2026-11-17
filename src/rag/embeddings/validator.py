import math


class EmbeddingValidator:
    @staticmethod
    def validate(
        vector: list[float],
        expected_dimensions: int,
    ) -> None:

        if len(vector) != expected_dimensions:
            raise ValueError("Invalid embedding dimensions")

        if not vector:
            raise ValueError("Empty embedding")

        for value in vector:
            if not math.isfinite(value):
                raise ValueError("Embedding contains invalid values")
