from psycopg import Connection

from consensus_curator.models.raw_document import RawDocument


def save_raw_document(doc: RawDocument, conn: Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw_documents (id, source_type, url, domain, title, 
                                        published_at, content, fetched_at)
            VALUES (%(id)s, %(source_type)s, %(url)s, %(domain)s, %(title)s, %(published_at)s, 
                    %(content)s, %(fetched_at)s)
            ON CONFLICT (id) DO NOTHING
            """,
            doc.model_dump(),
        )
