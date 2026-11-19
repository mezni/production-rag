class QueryPreprocessor:
    @staticmethod
    def process(query: str) -> str:

        normalized = " ".join(query.split())

        return normalized.strip()
