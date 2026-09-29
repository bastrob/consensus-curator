CREATE TABLE IF NOT EXISTS documents (
    raw_document_id CHAR(16) PRIMARY KEY references raw_documents(id),
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    published_at TIMESTAMPTZ NULL,
    synthesis TEXT NOT NULL,
    model TEXT NOT NULL,
    created_at TIMESTAMPTZ
)