import argparse

from consensus_curator.application.pipelines.extraction_pipeline import run_extraction_pipeline
from consensus_curator.collectors.rss import RSSCollector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed", action="append", required=True, dest="feeds")
    parser.add_argument("--max-documents", type=int, default=5)
    args = parser.parse_args()

    collector = RSSCollector(feed_urls=args.feeds)
    run_extraction_pipeline(collector=collector, max_documents=args.max_documents)


if __name__ == "__main__":
    main()
