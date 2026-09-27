"""
Every collector implements this Protocol. `source_type` stays a plain string
(not an enum) deliberately at this stage — enumerating source types up front
means editing a shared enum every time a new collector is added, which
couples unrelated collector modules through a single import.
"""

from typing import Protocol

from consensus_curator.models.raw_document import RawDocument


class Collector(Protocol):
    source_type: str

    def fetch(self, topic: str, max_documents: int = 20) -> list[RawDocument]:
        """
        Fetch and normalize documents relevant to `topic`.

        Implementations own their own relevance filtering (e.g. RSS collector
        filters entries by keyword match against the topic before the more
        expensive fetch+clean step) — callers should be able to assume
        everything returned is at least plausibly on-topic, not run a second
        relevance pass themselves.
        """
        ...
