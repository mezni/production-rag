from types import SimpleNamespace
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from rag.vector_store.postgres_repository import PostgresVectorRepository


@pytest.fixture
def repository():
    return PostgresVectorRepository(MagicMock())


def test_invalid_embedding_dimension(repository):
    with pytest.raises(ValueError):
        repository.search(
            query_embedding=[0.1, 0.2],
            limit=5,
            tenant_id="tenant-1",
        )


def test_invalid_search_limit(repository):
    with pytest.raises(ValueError):
        repository.search(
            query_embedding=[0.1] * 1536,
            limit=0,
            tenant_id="tenant-1",
        )


def test_missing_tenant_id(repository):
    with pytest.raises(ValueError):
        repository.search(
            query_embedding=[0.1] * 1536,
            limit=5,
        )


def test_search_returns_rows_for_tenant():
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    chunk_id = uuid4()
    document_id = uuid4()
    cursor.description = [
        SimpleNamespace(name="chunk_id"),
        SimpleNamespace(name="document_id"),
        SimpleNamespace(name="content"),
        SimpleNamespace(name="metadata"),
        SimpleNamespace(name="filename"),
        SimpleNamespace(name="distance"),
    ]
    cursor.fetchall.return_value = [
        (
            chunk_id,
            document_id,
            "Refund policy",
            {"chunk_index": 1},
            "policy.pdf",
            0.25,
        )
    ]
    repository = PostgresVectorRepository(connection, dimensions=3)

    results = repository.search(
        query_embedding=[0.1, 0.2, 0.3],
        limit=2,
        tenant_id="tenant-1",
    )

    assert results == [
        {
            "chunk_id": chunk_id,
            "document_id": document_id,
            "content": "Refund policy",
            "metadata": {"chunk_index": 1},
            "filename": "policy.pdf",
            "distance": 0.25,
        }
    ]
    params = cursor.execute.call_args.args[1]
    assert params[1] == "tenant-1"
    assert params[3] == 2
