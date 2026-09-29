import argparse

from consensus_curator.application.pipelines.summarizer_pipeline import run_summarizer_pipeline
from consensus_curator.summarizers import OllamaSummarizer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--base-url", default="http://localhost:11434/v1")
    args = parser.parse_args()

    summarizer = OllamaSummarizer(model_name=args.model_name, base_url=args.base_url)
    run_summarizer_pipeline(summarizer)


if __name__ == "__main__":
    main()
