from rag.chunking.strategies.fixed_size import FixedSizeChunker


def test_fixed_size_chunking():

    chunker = FixedSizeChunker(
        chunk_size=10,
        overlap=2,
    )

    chunks = chunker.chunk(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "doc-001",
    )

    assert len(chunks) > 1
    assert chunks[0].content == "ABCDEFGHIJ"
    assert chunks[1].content == "IJKLMNOPQR"
