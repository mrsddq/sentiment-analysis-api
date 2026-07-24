from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .analyzer import SentimentAnalyzer


app = FastAPI(title="Sentiment Analysis API", version="0.1.0")
analyzer = SentimentAnalyzer()


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)


class BatchRequest(BaseModel):
    texts: list[str] = Field(min_length=1, max_length=100)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze")
def analyze(request: TextRequest) -> dict[str, object]:
    return analyzer.analyze(request.text).to_dict()


@app.post("/v1/analyze/batch")
def analyze_batch(request: BatchRequest) -> dict[str, object]:
    results = [analyzer.analyze(text).to_dict() for text in request.texts]
    counts = {label: sum(result["label"] == label for result in results) for label in ("positive", "neutral", "negative")}
    return {"results": results, "summary": counts}

