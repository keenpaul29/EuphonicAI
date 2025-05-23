from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from ..services.recommender import MoodRecommender
from ..ml_models.mood_classifier import MoodClassifier
import numpy as np
import logging

music_router = APIRouter()
recommender = MoodRecommender()
mood_classifier = MoodClassifier()

class TrackAnalysis(BaseModel):
    track_id: str

@music_router.get("/recommendations/mood/{mood}")
async def get_mood_recommendations(
    mood: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """Get song recommendations based on mood"""
    try:
        recommendations = recommender.get_recommendations_by_mood(mood, limit)
        return {
            'status': 'success',
            'recommendations': recommendations
        }
    except Exception as e:
        logging.error(f"Error getting mood recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@music_router.get("/recommendations/similar/{track_id}")
async def get_similar_songs(
    track_id: str,
    limit: int = Query(default=5, ge=1, le=20)
):
    """Get similar songs based on a track ID"""
    try:
        similar_songs = recommender.get_similar_songs(track_id, limit)
        return {
            'status': 'success',
            'similar_songs': similar_songs
        }
    except Exception as e:
        logging.error(f"Error getting similar songs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@music_router.post("/analyze")
async def analyze_track(track: TrackAnalysis):
    """Analyze a track's mood based on its audio features"""
    try:
        features = recommender.get_audio_features(track.track_id)
        if not features:
            raise HTTPException(
                status_code=404,
                detail='Could not fetch audio features'
            )

        # Convert features to the format expected by the mood classifier
        feature_vector = [
            features['valence'],
            features['energy'],
            features['danceability'],
            features['tempo'],
            features['instrumentalness'],
            features['acousticness']
        ]
        
        predicted_mood = mood_classifier.predict_mood(np.array(feature_vector))
        
        return {
            'status': 'success',
            'track_id': track.track_id,
            'predicted_mood': predicted_mood,
            'audio_features': features
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error analyzing track: {e}")
        raise HTTPException(status_code=500, detail=str(e))
