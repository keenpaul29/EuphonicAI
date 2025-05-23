import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)

class TextSentimentAnalyzer:
    def __init__(self):
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> dict:
        """
        Analyze the sentiment of the given text and map it to a mood.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Contains sentiment scores and mapped mood
        """
        try:
            scores = self.analyzer.polarity_scores(text)
            mood = self._map_sentiment_to_mood(scores)
            return {
                'sentiment_scores': scores,
                'mood': mood
            }
        except Exception as e:
            logger.error(f"Error analyzing text sentiment: {e}")
            raise

    def _map_sentiment_to_mood(self, scores: dict) -> str:
        """
        Map VADER sentiment scores to music moods.
        
        Args:
            scores (dict): VADER sentiment scores
            
        Returns:
            str: Mapped mood suitable for music recommendation
        """
        compound = scores['compound']
        
        if compound >= 0.5:
            return 'happy'
        elif compound <= -0.5:
            return 'sad'
        elif compound >= 0.1:
            return 'energetic'
        elif compound <= -0.1:
            return 'calm'
        else:
            return 'chill'  # neutral sentiment

    def get_supported_moods(self) -> list:
        """
        Return list of supported moods for text sentiment analysis.
        """
        return ['happy', 'sad', 'energetic', 'calm', 'chill']
