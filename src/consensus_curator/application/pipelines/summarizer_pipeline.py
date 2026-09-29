from loguru import logger

from consensus_curator.models import Document
from consensus_curator.storage.connection import get_connection
from consensus_curator.storage.document_repository import get_documents_to_summarize, save_document
from consensus_curator.summarizers import Summarizer


def run_summarizer_pipeline(summarizer: Summarizer):
    conn = get_connection()
    try:
        for raw_document in get_documents_to_summarize(conn):
            try:
                synthesis = summarizer.summarize(raw_document)
                doc = Document(
                    raw_document_id=raw_document.id,
                    url=raw_document.url,
                    title=raw_document.title,
                    published_at=raw_document.published_at,
                    synthesis=synthesis,
                    model=summarizer.model_name,
                )
                save_document(doc, conn)
                conn.commit()
                logger.info(f"Summarized {raw_document.url} -> {doc.synthesis[:200]}")
            except Exception:
                conn.rollback()
                logger.exception(f"Failed to summarize {raw_document.url}")
    finally:
        conn.close()
