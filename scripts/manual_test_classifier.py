import argparse

from consensus_curator.application.pipelines.classifier_pipeline import run_classifier_pipeline
from consensus_curator.classifiers import OllamaClassifier
from consensus_curator.storage.connection import get_connection
from consensus_curator.storage.topic_repository import get_all_topics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--base-url", default="http://localhost:11434/v1")
    args = parser.parse_args()

    conn = get_connection()
    try:
        topics = get_all_topics(conn)
    finally:
        conn.close()

    classifier = OllamaClassifier(topics=topics, model_name=args.model_name, base_url=args.base_url)
    run_classifier_pipeline(classifier)


if __name__ == "__main__":
    main()
