from typing import Protocol

from consensus_curator.models.document import Document


class Classifier(Protocol):
    model_name: str

    def classify(self, document: Document) -> list[str]:
        """
        Assign zero or more topics to a Document, drawn from the closed
        topic ontology maintained in the `topics` table.

        Implementations are responsible for their own LLM/backend details
        (prompt, retries, constrained decoding) but must only return slugs
        that exist in the ontology — never a label the model invented.
        An empty list is a valid result: it means the document doesn't
        match any topic currently tracked, not a failure.
        """
        ...
