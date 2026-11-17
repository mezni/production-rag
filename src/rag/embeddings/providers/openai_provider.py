from openai import OpenAI


class OpenAIEmbeddingProvider:
    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ):
        self.client = OpenAI()
        self.model = model

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        ordered = sorted(
            response.data,
            key=lambda item: item.index,
        )

        return [item.embedding for item in ordered]
