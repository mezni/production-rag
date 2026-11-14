import pytest

from rag.chunking.config import ChunkingConfig


def test_default_configuration():
    config = ChunkingConfig()

    assert config.chunk_size == 1000
    assert config.chunk_overlap == 150


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        ChunkingConfig(chunk_size=100, chunk_overlap=100)


def test_chunk_size_must_be_positive():
    with pytest.raises(ValueError):
        ChunkingConfig(chunk_size=0)
