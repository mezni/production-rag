import pytest

from rag.retrieval.evaluation import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_precision_at_k():
    relevant = {"a", "c"}
    retrieved = ["a", "b", "c", "d"]

    assert precision_at_k(relevant, retrieved, 3) == 2 / 3


def test_precision_at_k_with_no_results():
    assert precision_at_k({"a"}, [], 3) == 0.0


def test_precision_at_k_rejects_invalid_k():
    with pytest.raises(ValueError):
        precision_at_k({"a"}, ["a"], 0)


def test_recall_at_k():
    relevant = {"a", "c", "e"}
    retrieved = ["a", "b", "c", "d"]

    assert recall_at_k(relevant, retrieved, 3) == 2 / 3
    assert recall_at_k(relevant, retrieved, 5) == 2 / 3


def test_recall_at_k_with_no_relevant_ids():
    assert recall_at_k(set(), ["a"], 3) == 0.0


def test_recall_at_k_rejects_invalid_k():
    with pytest.raises(ValueError):
        recall_at_k({"a"}, ["a"], 0)


def test_reciprocal_rank():
    relevant = {"b", "c"}
    retrieved = ["a", "b", "c"]

    assert reciprocal_rank(relevant, retrieved) == 0.5


def test_reciprocal_rank_without_relevant_result():
    assert reciprocal_rank({"z"}, ["a", "b"]) == 0.0
