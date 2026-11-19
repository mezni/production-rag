from typing import ClassVar


class RecursiveCharacterSplitter:
    SEPARATORS: ClassVar[list[str]] = ["\n\n", "\n", ". ", " ", ""]

    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        min_boundary_ratio: float = 0.5,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_boundary_ratio = min_boundary_ratio

    def split(self, text: str) -> list[tuple[str, int, int]]:
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            max_end = min(start + self.chunk_size, text_length)

            if max_end == text_length:
                end = text_length
            else:
                end = self._find_boundary(text, start, max_end)

            if end <= start:
                raise RuntimeError("Chunk splitter made no progress")

            chunks.append((text[start:end], start, end))

            if end == text_length:
                break

            next_start = max(start + 1, end - self.chunk_overlap)
            start = next_start

        return chunks

    def _find_boundary(
        self,
        text: str,
        start: int,
        max_end: int,
    ) -> int:
        minimum_end = start + int(self.chunk_size * self.min_boundary_ratio)

        for separator in self.SEPARATORS:
            if not separator:
                continue

            position = text.rfind(
                separator,
                minimum_end,
                max_end,
            )

            if position != -1:
                return position + len(separator)

        return max_end
