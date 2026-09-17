# Sentiment Analysis API

An explainable sentiment service that returns a normalized score, confidence, label, and the words that influenced the result. It runs without model downloads or external APIs.

## Highlights

- Single and batch FastAPI endpoints
- Negation, intensifiers, dampeners, capitalization, and emoticon handling
- Explainable positive and negative token hits
- Request limits and generated OpenAPI documentation
- CLI, Docker image, tests, and CI

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn sentiment_api.api:app --reload
```

```bash
curl -X POST http://localhost:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The onboarding was absolutely excellent!"}'
```

Example result:

```json
{
  "label": "positive",
  "score": 0.6965,
  "confidence": 0.8482,
  "positive_hits": ["excellent"],
  "negative_hits": []
}
```

Batch up to 100 items with `POST /v1/analyze/batch`, or run `sentiment "not very helpful"` from a terminal.

## Design notes

This is a transparent baseline suited to demos, routing, and monitoring. For domain-specific production use, calibrate the lexicon against labeled examples or replace `SentimentAnalyzer` behind the same API contract with a trained model.

```bash
pytest
ruff check .
docker build -t sentiment-api .
```

MIT licensed.

## Contract and model limitations

Single and batch inputs share the same trimmed, nonempty 20,000-character limit. Batches
preserve input order, accept at most 100 items, and have a 100,000-character aggregate budget.
The test suite checks HTTP rejection, batch ordering/counts, emoticons, and sentence-scoped negation.

`confidence` is a heuristic derived from score magnitude, **not a calibrated probability** or
measured accuracy. This English lexicon baseline has no learned weights, model training, or
external inference calls. Sarcasm, domain vocabulary, language changes, and long-distance negation
can fail. Before using it for a consequential decision, evaluate labeled domain data and compare
against a trained baseline; no production accuracy or throughput is claimed here.
