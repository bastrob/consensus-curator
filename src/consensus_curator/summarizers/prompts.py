SUMMARY_PROMPT = """You are summarizing a news article for an automated pipeline that will later compare and combine it with articles from other sources on the same topic.

Write a concise summary (3-5 sentences) that preserves every concrete, verifiable detail from the article: named people, organizations, products, exact figures, dates, and direct claims attributed to a named source. Omit background context, editorializing, and stylistic flourishes that don't carry factual content.

Do not add any information that is not in the article. Do not speculate about implications. Write in plain English, as a sequence of factual statements rather than a narrative.
"""
