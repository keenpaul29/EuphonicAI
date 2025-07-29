from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ..services.text_sentiment import TextSentimentAnalyzer
from ..services.spotify_service import generate_mood_playlist

router = APIRouter()
sentiment_analyzer = TextSentimentAnalyzer()

class TextAnalysisRequest(BaseModel):
    text: str
    limit: Optional[int] = 10
    language: Optional[str] = None

class TextAnalysisResponse(BaseModel):
    sentiment_scores: dict
    mood: str
    recommendations: List[dict]

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text_and_recommend(request: TextAnalysisRequest):
    """
    Analyze text sentiment and return music recommendations based on the detected mood.
    """
    try:
        # Analyze text sentiment
        analysis = sentiment_analyzer.analyze_text(request.text)
        
        # Get song recommendations based on the detected mood
        recommendations = await generate_mood_playlist(
            mood=analysis['mood'],
            limit=request.limit
        )
        
        # Convert recommendations to dict format
        recommendations_dict = [
            {
                'id': track.id,
                'name': track.name,
                'artists': [{'name': artist.name, 'id': artist.id} for artist in track.artists],
                'uri': track.uri,
                'preview_url': track.preview_url,
                'image_url': track.image_url
            }
            for track in recommendations
        ]
        
        return {
            'sentiment_scores': analysis['sentiment_scores'],
            'mood': analysis['mood'],
            'recommendations': recommendations_dict
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
