from loguru import logger

from consensus_curator.classifiers import Classifier
from consensus_curator.storage.connection import get_connection
from consensus_curator.storage.topic_repository import (
    get_documents_to_classify,
    save_document_topics,
)


def run_classifier_pipeline(classifier: Classifier):
    conn = get_connection()
    try:
        for doc in get_documents_to_classify(conn):
            try:
                topic_slugs = classifier.classify(doc)
                save_document_topics(doc.raw_document_id, topic_slugs, conn)
                conn.commit()
            except Exception:
                conn.rollback()
                logger.exception(f"Failed to classify {doc.url}")
    finally:
        conn.close()
