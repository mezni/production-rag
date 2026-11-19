from dataclasses import FrozenInstanceError

import pytest

from rag.retrieval.filters import RetrievalFilters


def test_default_filters():
    filters = RetrievalFilters(tenant_id="tenant-1")

    assert filters.tenant_id == "tenant-1"
    assert filters.department is None
    assert filters.document_type is None


def test_filters_with_metadata():
    filters = RetrievalFilters(
        tenant_id="tenant-1",
        department="legal",
        document_type="contract",
    )

    assert filters.department == "legal"
    assert filters.document_type == "contract"


def test_filters_are_immutable():
    filters = RetrievalFilters(tenant_id="tenant-1")

    with pytest.raises(FrozenInstanceError):
        filters.tenant_id = "tenant-2"
