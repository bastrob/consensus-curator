CREATE TABLE IF NOT EXISTS document_topics (
    raw_document_id CHAR(16) REFERENCES raw_documents(id),
    topic_slug TEXT REFERENCES topics(slug),
    PRIMARY KEY (raw_document_id, topic_slug)
)