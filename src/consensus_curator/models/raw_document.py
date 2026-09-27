import hashlib
from datetime import datetime

from pydantic import BaseModel, Field, computed_field


class RawDocument(BaseModel):
    source_type: str  # v1 "rss" for now
    domain: str
    url: str
    title: str
    published_at: datetime | None
    content: str
    fetched_at: datetime = Field(default_factory=datetime.now)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        # Content hash, not URL: the same URL can be re-scraped with edited
        # content (news orgs correct articles post-publication); we want a
        # new id in that case rather than silently deduping against stale text.
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()[:16]
