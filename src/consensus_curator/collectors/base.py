"""
Every collector implements this Protocol. `source_type` stays a plain string
(not an enum) deliberately at this stage — enumerating source types up front
means editing a shared enum every time a new collector is added, which
couples unrelated collector modules through a single import.
"""

from collections.abc import Iterator
from typing import Protocol

from consensus_curator.models import RawDocument


class Collector(Protocol):
    source_type: str

    def fetch(self) -> Iterator[RawDocument]:
        """
        Fetch all available documents from this source, unfiltered.

        Implementations are responsible for their own source-specific
        details (parsing, retries, per-entry failure handling) but must not
        filter by topic or relevance — that's the Selector's job downstream.
        Callers should assume everything yielded is raw and unvalidated for
        relevance; results are persisted as-is by the calling pipeline.
        """
        ...
