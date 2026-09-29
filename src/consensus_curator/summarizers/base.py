from typing import Protocol

from consensus_curator.models import RawDocument


class Summarizer(Protocol):
    model_name: str

    def summarize(self, raw_document: RawDocument) -> str:
        """
        Summarize a RawDocument into a concise synthesis.

        Implementations are responsible for their own LLM/backend details
        (prompt, retries, timeouts) but must return a plain-text summary —
        callers (the summarizer pipeline) know nothing about how it was
        produced, only that it's usable as `Document.synthesis`.
        """
        ...
