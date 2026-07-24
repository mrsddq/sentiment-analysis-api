import argparse
import json

from .analyzer import SentimentAnalyzer


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze the sentiment of text")
    parser.add_argument("text", nargs="+")
    args = parser.parse_args()
    result = SentimentAnalyzer().analyze(" ".join(args.text))
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()

