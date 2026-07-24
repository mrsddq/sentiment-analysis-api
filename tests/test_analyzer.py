from sentiment_api import SentimentAnalyzer


analyzer = SentimentAnalyzer()


def test_positive_sentiment_is_explainable():
    result = analyzer.analyze("The support was absolutely excellent and very helpful!")
    assert result.label == "positive"
    assert "excellent" in result.positive_hits
    assert result.score > 0.5


def test_negative_sentiment():
    result = analyzer.analyze("This is the worst, most confusing flow.")
    assert result.label == "negative"
    assert result.score < -0.3


def test_negation_changes_polarity():
    positive = analyzer.analyze("This is good")
    negated = analyzer.analyze("This is not good")
    assert positive.score > 0
    assert negated.score < 0


def test_unknown_words_are_neutral():
    assert analyzer.analyze("The parcel arrived on Tuesday").label == "neutral"

