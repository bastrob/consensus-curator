import argparse
import logging

from src.consensus_curator.collectors.rss import RSSCollector

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--feed", action="append", required=True, dest="feeds")
    parser.add_argument("--max-documents", type=int, default=5)
    args = parser.parse_args()

    collector = RSSCollector(feed_urls=args.feeds)
    documents = collector.fetch(topic=args.topic, max_documents=args.max_documents)

    logger.info(f"{len(documents)} documents collected.")

    for doc in documents:
        logger.info(f"title: {doc.title}, url: {doc.url}")


if __name__ == "__main__":
    main()
