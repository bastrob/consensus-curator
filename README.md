# Consensus Curator

## Setup

```bash
pyenv install 3.11.9   # if not already installed
poetry env use 3.11.9
poetry install
cp .env.example .env   
```

## Status: v1 in progress

Implemented:
- `collectors/rss.py` — RSS feed collection with keyword relevance
  pre-filter and per-entry failure isolation.
  
## Validate the collector + extractor by hand before wiring the graph

```bash
poetry run python -m scripts.manual_test_extraction \
    --feed https://openai.com/blog/rss.xml \
    --max-documents 3
```