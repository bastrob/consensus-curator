from psycopg import Connection
from psycopg.rows import dict_row

from consensus_curator.models import Document, Topic


def get_all_topics(conn: Connection) -> list[Topic]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM topics")
        return [Topic.model_validate(row) for row in cur.fetchall()]


def get_documents_to_classify(conn: Connection) -> list[Document]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM documents WHERE classified_at IS NULL")
        return [Document.model_validate(row) for row in cur.fetchall()]


def save_document_topics(raw_document_id: str, topic_slugs: list[str], conn: Connection):
    with conn.cursor() as cur:
        for slug in topic_slugs:
            cur.execute(
                "INSERT INTO document_topics (raw_document_id, topic_slug) VALUES (%s, %s)",
                (raw_document_id, slug),
            )
        cur.execute(
            "UPDATE documents SET classified_at = now() WHERE raw_document_id = %s",
            (raw_document_id,),
        )
