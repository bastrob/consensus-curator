CLASSIFICATION_PROMPT = """You are classifying a document against a fixed, closed list of topics. Your job is to decide which of these topics, if any, the document is genuinely about — not to invent new ones.

Available topics:
{topics_list}

Rules:
- Only use topic slugs from the list above. Never invent a new topic or rename an existing one.
- A document can match zero, one, or several topics. If none of the topics genuinely apply, return an empty list — do not force a match.
- A topic applies only if the document is substantially about it, not merely mentions it in passing.

Respond with a JSON array of topic slugs only, nothing else. Example: ["ai-agents", "coding-tools"] or [].
"""
