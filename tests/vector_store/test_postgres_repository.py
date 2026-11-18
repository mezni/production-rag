from unittest.mock import MagicMock

import pytest

from rag.vector_store.postgres_repository import (
    PostgresVectorRepository,
)


@pytest.fixture
def repository():
    return PostgresVectorRepository(MagicMock())


def test_invalid_embedding_dimension(repository):

    with pytest.raises(ValueError):
        repository.search(
            query_embedding=[0.1, 0.2],
            limit=5,
        )


def test_invalid_search_limit(repository):

    with pytest.raises(ValueError):
        repository.search(
            query_embedding=[0.1] * 1536,
            limit=0,
        )
