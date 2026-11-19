def precision_at_k(
    relevant_ids: set[str],
    retrieved_ids: list[str],
    k: int,
) -> float:

    if k <= 0:
        raise ValueError("k must be positive")

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(item in relevant_ids for item in retrieved)

    return relevant_count / len(retrieved)


def recall_at_k(
    relevant_ids: set[str],
    retrieved_ids: list[str],
    k: int,
) -> float:

    if k <= 0:
        raise ValueError("k must be positive")

    if not relevant_ids:
        return 0.0

    retrieved = retrieved_ids[:k]

    relevant_count = sum(item in relevant_ids for item in retrieved)

    return relevant_count / len(relevant_ids)


def reciprocal_rank(
    relevant_ids: set[str],
    retrieved_ids: list[str],
) -> float:

    for rank, item in enumerate(retrieved_ids, start=1):
        if item in relevant_ids:
            return 1.0 / rank

    return 0.0
