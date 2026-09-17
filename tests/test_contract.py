import pytest
from fastapi.testclient import TestClient

from sentiment_api.analyzer import SentimentAnalyzer
from sentiment_api.api import app

client = TestClient(app)


@pytest.mark.parametrize("text", ["", "   ", "x" * 20_001])
def test_single_and_batch_enforce_same_text_bounds(text):
    assert client.post("/v1/analyze", json={"text": text}).status_code == 422
    assert client.post("/v1/analyze/batch", json={"texts": [text]}).status_code == 422


def test_batch_budget_is_enforced():
    assert client.post("/v1/analyze/batch", json={"texts": ["x" * 20_000] * 6}).status_code == 422


def test_batch_preserves_order_and_counts():
    response = client.post("/v1/analyze/batch", json={"texts": ["good", "terrible", "desk"]})
    assert response.status_code == 200
    payload = response.json()
    assert [item["label"] for item in payload["results"]] == ["positive", "negative", "neutral"]
    assert payload["summary"] == {"positive": 1, "negative": 1, "neutral": 1}


def test_smiling_emoticon_is_scored():
    assert SentimentAnalyzer().analyze(":D").label == "positive"


def test_negation_does_not_cross_sentence_boundary():
    assert SentimentAnalyzer().analyze("Not here. Excellent!").label == "positive"
    assert SentimentAnalyzer().analyze("not excellent").label == "negative"
