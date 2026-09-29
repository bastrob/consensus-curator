from itertools import islice

from loguru import logger

from consensus_curator.collectors import RSSCollector
from consensus_curator.storage.connection import get_connection
from consensus_curator.storage.raw_document_repository import save_raw_document


def run_extraction_pipeline(collector: RSSCollector, max_documents: int | None = None) -> None:
    conn = get_connection()
    try:
        for doc in islice(collector.fetch(), max_documents):
            try:
                save_raw_document(doc, conn)
                conn.commit()
            except Exception:
                conn.rollback()
                logger.exception(f"Failed to save document from source {doc.url}")
    finally:
        conn.close()
