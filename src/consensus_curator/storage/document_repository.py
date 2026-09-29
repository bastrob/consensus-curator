from psycopg import Connection
from psycopg.rows import dict_row

from consensus_curator.models import Document, RawDocument


def save_document(doc: Document, conn: Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO documents (raw_document_id, url, title, 
                                        published_at, synthesis, model, created_at)
            VALUES (%(raw_document_id)s, %(url)s, %(title)s, %(published_at)s, 
                    %(synthesis)s, %(model)s, %(created_at)s)
            """,
            doc.model_dump(),
        )


def get_document(conn: Connection):
    pass


def get_documents_to_summarize(conn: Connection) -> list[RawDocument]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT rd.*
            FROM raw_documents rd
            LEFT JOIN documents ON rd.id = documents.raw_document_id
            WHERE documents.raw_document_id IS NULL
            """
        )
        rows = cur.fetchall()

        return [RawDocument.model_validate(row) for row in rows]
