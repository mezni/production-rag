from uuid import UUID, uuid4

from pgvector import Vector
from psycopg import Connection


class PostgresVectorRepository:
    def __init__(
        self,
        connection: Connection,
        dimensions: int = 1536,
    ):
        self.connection = connection
        self.dimensions = dimensions

    def save(
        self,
        chunk_id: UUID,
        embedding: list[float],
        model_name: str,
    ) -> None:

        if len(embedding) != self.dimensions:
            raise ValueError("Invalid embedding dimensions")

        query = """
            INSERT INTO chunk_embeddings (
                id,
                chunk_id,
                embedding,
                model_name,
                dimensions
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id)
            DO UPDATE SET
                embedding = EXCLUDED.embedding,
                model_name = EXCLUDED.model_name,
                dimensions = EXCLUDED.dimensions,
                created_at = NOW()
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    uuid4(),
                    chunk_id,
                    Vector(embedding),
                    model_name,
                    self.dimensions,
                ),
            )

        self.connection.commit()

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
        tenant_id: str | None = None,
    ) -> list[dict]:

        if len(query_embedding) != self.dimensions:
            raise ValueError("Invalid embedding dimensions")

        if limit <= 0:
            raise ValueError("Limit must be positive")

        if not tenant_id:
            raise ValueError("Tenant ID is required")

        query = """
            SELECT
                dc.id AS chunk_id,
                dc.document_id,
                dc.content,
                dc.metadata,
                d.filename,
                ce.embedding <=> %s AS distance

            FROM chunk_embeddings ce

            JOIN document_chunks dc
                ON dc.id = ce.chunk_id

            JOIN documents d
                ON d.id = dc.document_id

            WHERE d.status = 'indexed'
              AND d.tenant_id = %s

            ORDER BY ce.embedding <=> %s

            LIMIT %s
        """

        vector = Vector(query_embedding)

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    vector,
                    tenant_id,
                    vector,
                    limit,
                ),
            )

            columns = [description.name for description in cursor.description]

            return [dict(zip(columns, row)) for row in cursor.fetchall()]
