from openai import OpenAI

from consensus_curator.models import RawDocument
from consensus_curator.summarizers.prompts import SUMMARY_PROMPT


class OllamaSummarizer:
    """
    Summarizer backed by a local Ollama server, accessed through its
    OpenAI-compatible API.

    Design choices worth flagging:
    - Uses the `openai` client rather than an Ollama-specific SDK: swapping
      to a hosted OpenAI-compatible provider later means changing
      `base_url` only, not this class.
    - No retry/timeout handling here — a transient failure (model still
      loading, request timeout) surfaces as an exception and is caught by
      the calling pipeline, which logs it and moves to the next document.
      If a specific failure mode proves common in practice, that's the
      signal to add retry logic here rather than anticipate it now.
    """

    def __init__(self, model_name: str = "qwen3.5:9b", base_url: str = "http://localhost:11434/v1"):
        self.model_name = model_name
        self._client = OpenAI(base_url=base_url, api_key="ollama")

    def summarize(self, raw_document: RawDocument) -> str:
        chat_completion = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": SUMMARY_PROMPT},
                {"role": "user", "content": raw_document.content},
            ],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content
