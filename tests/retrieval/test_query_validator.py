import pytest

from rag.retrieval.query_validator import QueryValidator


def test_valid_query():
    QueryValidator.validate("Refund policy")


@pytest.mark.parametrize("query", ["", "   \n\t"])
def test_empty_query(query):
    with pytest.raises(ValueError, match="empty"):
        QueryValidator.validate(query)


def test_query_over_limit():
    with pytest.raises(ValueError, match="long"):
        QueryValidator.validate("x" * (QueryValidator.MAX_QUERY_LENGTH + 1))
