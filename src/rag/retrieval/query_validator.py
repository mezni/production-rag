class QueryValidator:
    MAX_QUERY_LENGTH = 5000

    @classmethod
    def validate(cls, query: str) -> None:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if len(query) > cls.MAX_QUERY_LENGTH:
            raise ValueError("Query is too long")
