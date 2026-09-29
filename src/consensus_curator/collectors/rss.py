from collections.abc import Iterator
from datetime import datetime
from time import mktime
from urllib.parse import urlparse

import feedparser
import trafilatura
from loguru import logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from consensus_curator.models import RawDocument


class RSSCollector:
    """
    Collector for RSS/Atom feeds.

    Design choices worth flagging:
    - Relevance filtering happens BEFORE the expensive trafilatura fetch,
      on title+summary only. This is a cheap keyword match, not semantic —
      good enough for v1, and it bounds cost: a feed with 200 entries where
      3 mention the topic shouldn't trigger 200 full-page fetches.
    - Per-entry failures (dead link, paywall, parse failure) are caught and
      logged, not raised — one bad entry in a feed of 50 should not abort
      the whole collection run. This is the "recoverability" principle from
      the design doc, implemented at the smallest possible granularity.
    - No dedup across feeds here (e.g. two feeds syndicating the same wire
      story) — that's the consensus stage's job (distinct-domain counting),
      not the collector's. Collectors report what they found; scoring
      decides what it's worth.
    """

    source_type = "rss"

    def __init__(self, feed_urls: list[str]):
        if not feed_urls:
            raise ValueError("RSSCollector requires at least one feed URL.")
        self.feed_urls = feed_urls

    def fetch(self) -> Iterator[RawDocument]:
        documents: list[RawDocument] = []

        for feed_url in self.feed_urls:
            for entry in self._parse_feed(feed_url):
                doc = self._entry_to_document(entry)
                if doc is not None:
                    yield doc

        logger.info(
            f"RSSCollector: {len(documents)} relevant documents collected "
            f"across {len(self.feed_urls)} feeds"
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True,
    )
    def _parse_feed(self, feed_url: str) -> list[feedparser.FeedParserDict]:
        parsed = feedparser.parse(feed_url)
        if parsed.bozo and not parsed.entries:
            logger.warning(f"Feed unreachable or malformed, skipping: {feed_url}")
            return []
        return parsed.entries

    def _entry_to_document(self, entry: feedparser.FeedParserDict) -> RawDocument | None:
        url = entry.get("link")
        if not url:
            return None

        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                logger.warning(f"Could not download article body: {url}")
                return None

            content = trafilatura.extract(downloaded, favor_precision=True)
            if not content or len(content.strip()) < 200:
                # Below this length it's almost always a stub/teaser page,
                # not real article body — not worth extracting claims from.
                logger.info("Extracted content too short, skipping: %s", url)
                return None

            published_at = None
            if getattr(entry, "published_parsed", None):
                published_at = datetime.fromtimestamp(mktime(entry.published_parsed))

            return RawDocument(
                source_type=self.source_type,
                url=url,
                domain=urlparse(url).netloc,
                title=entry.get("title", "").strip(),
                published_at=published_at,
                content=content.strip(),
            )

        except Exception:
            logger.exception("Failed to process entry %s, skipping", url)
            return None
