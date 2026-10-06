import json

from loguru import logger
from openai import OpenAI

from consensus_curator.classifiers.prompts import CLASSIFICATION_PROMPT
from consensus_curator.models.document import Document
from consensus_curator.models.topic import Topic


class OllamaClassifier:
    def __init__(
        self,
        topics: list[Topic],
        model_name: str = "qwen3.5:9b",
        base_url: str = "http://localhost:11434/v1",
    ):
        self.model_name = model_name
        self.topics = topics
        self._valid_slugs = {t.slug for t in self.topics}
        self._client = OpenAI(base_url=base_url, api_key="ollama")

        topic_list = "\n".join(f"- {t.slug}: {t.label}" for t in self.topics)
        self._system_prompt = CLASSIFICATION_PROMPT.format(topics_list=topic_list)

    def classify(self, document: Document) -> list[str]:
        user_prompt = f"Document title: {document.title}\nDocument summary: {document.synthesis}"
        chat_completion = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": CLASSIFICATION_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            model=self.model_name,
            response_format={"type": "json_object"},
        )

        raw_slugs = json.loads(chat_completion.choices[0].message.content)
        valid = [s for s in raw_slugs if s in self._valid_slugs]
        invalid = [s for s in raw_slugs if s not in self._valid_slugs]
        if invalid:
            logger.warning(f"Classifier returned unknown topic slug for {document.url}: {invalid}")

        return valid
