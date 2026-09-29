CREATE TABLE IF NOT EXISTS raw_documents (
    id CHAR(16) PRIMARY KEY,
    source_type TEXT NOT NULL,
    url TEXT NOT NULL,
    domain TEXT NOT NULL,
    title TEXT NOT NULL,
    published_at TIMESTAMPTZ NULL,
    content TEXT NOT NULL,
    fetched_at TIMESTAMPTZ
)