from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'-]*|[:;]-?[)(DP/]")

POSITIVE = {
    "amazing": 2.5, "awesome": 2.5, "best": 2.4, "brilliant": 2.3,
    "delightful": 2.2, "enjoy": 1.6, "excellent": 2.6, "fantastic": 2.6,
    "fast": 0.7, "friendly": 1.5, "good": 1.5, "great": 2.0, "happy": 1.8,
    "helpful": 1.5, "impressive": 1.8, "love": 2.4, "loved": 2.4,
    "perfect": 2.5, "recommend": 1.5, "smooth": 1.2, "useful": 1.2,
    "win": 1.8, "wonderful": 2.5, ":)": 1.5, ":D": 2.0,
}
NEGATIVE = {
    "annoying": -1.8, "awful": -2.6, "bad": -1.7, "broken": -1.7,
    "confusing": -1.4, "disappointing": -2.0, "fail": -2.0, "failed": -2.0,
    "hate": -2.4, "horrible": -2.6, "poor": -1.6, "problem": -1.1,
    "refund": -1.2, "slow": -1.0, "terrible": -2.6, "unhelpful": -1.6,
    "useless": -2.0, "worst": -2.8, ":(": -1.5, ":/": -1.0,
}
NEGATIONS = {"not", "never", "no", "neither", "hardly", "isn't", "wasn't", "don't", "didn't"}
BOOSTERS = {"absolutely": 1.5, "extremely": 1.5, "really": 1.25, "very": 1.3, "so": 1.15}
DAMPENERS = {"barely": 0.5, "kind": 0.7, "slightly": 0.6, "somewhat": 0.7}


@dataclass(frozen=True)
class SentimentResult:
    label: str
    score: float
    confidence: float
    positive_hits: tuple[str, ...]
    negative_hits: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class SentimentAnalyzer:
    """Transparent lexicon sentiment with negation and intensity handling."""

    def analyze(self, text: str) -> SentimentResult:
        tokens = TOKEN_RE.findall(text)
        lowered = [token.lower() for token in tokens]
        total = 0.0
        positive_hits: list[str] = []
        negative_hits: list[str] = []

        for index, token in enumerate(lowered):
            value = POSITIVE.get(token, NEGATIVE.get(token, 0.0))
            if not value:
                continue
            window = lowered[max(0, index - 3):index]
            if any(word in NEGATIONS for word in window):
                value *= -0.85
            if index and lowered[index - 1] in BOOSTERS:
                value *= BOOSTERS[lowered[index - 1]]
            if index and lowered[index - 1] in DAMPENERS:
                value *= DAMPENERS[lowered[index - 1]]
            if token.isalpha() and tokens[index].isupper() and len(tokens[index]) > 1:
                value *= 1.2
            total += value
            (positive_hits if value > 0 else negative_hits).append(tokens[index])

        exclamations = min(text.count("!"), 3)
        if total:
            total += math.copysign(exclamations * 0.12, total)
        normalized = total / math.sqrt(total * total + 15) if total else 0.0
        label = "positive" if normalized >= 0.15 else "negative" if normalized <= -0.15 else "neutral"
        confidence = min(0.99, 0.5 + abs(normalized) / 2)
        return SentimentResult(
            label=label,
            score=round(normalized, 4),
            confidence=round(confidence, 4),
            positive_hits=tuple(positive_hits),
            negative_hits=tuple(negative_hits),
        )

