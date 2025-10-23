from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def contains_crisis(text: str) -> bool:
    crisis_keywords = [
        "suicide", "kill myself", "end my life",
        "can't go on", "hopeless", "want to die", "no reason to live"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in crisis_keywords)

def sentiment_score(text: str) -> dict:
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)
