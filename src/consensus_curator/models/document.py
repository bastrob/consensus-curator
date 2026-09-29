from datetime import datetime

from pydantic import BaseModel, Field


class Document(BaseModel):
    raw_document_id: str
    url: str
    title: str
    published_at: datetime | None
    model: str
    synthesis: str
    created_at: datetime = Field(default_factory=datetime.now)
