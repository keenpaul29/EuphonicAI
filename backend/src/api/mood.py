from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import traceback
import numpy as np

from ..services.emotion_detection import EmotionDetector, get_supported_emotions
from ..services.text_sentiment import TextSentimentAnalyzer
from ..services.spotify_service import fetch_random_tracks, validate_language, SpotifyTrack

logger = logging.getLogger(__name__)
mood_router = APIRouter()

class EmotionRequest(BaseModel):
    image: str
    language: Optional[str] = None

class TextAnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = None
    limit: Optional[int] = 10

class MoodDetectionResponse(BaseModel):
    emotion: str
    confidence: float
    playlist: List[SpotifyTrack]

# Mood Randomization Strategy
MOOD_RANDOMIZATION = {
    'happy': ['surprise', 'neutral', 'happy'],
    'sad': ['neutral', 'fear', 'sad'],
    'neutral': ['happy', 'sad', 'neutral'],
    'angry': ['surprise', 'fear', 'angry'],
    'surprise': ['happy', 'neutral', 'surprise'],
    'fear': ['sad', 'neutral', 'fear'],
    'disgust': ['angry', 'neutral', 'disgust']
}

def randomize_mood(detected_mood: str, confidence: float) -> str:
    """
    Randomize mood based on detected emotion and confidence.
    
    Args:
        detected_mood (str): Original detected mood
        confidence (float): Confidence of mood detection
    
    Returns:
        str: Potentially randomized mood
    """
    # Higher confidence means less randomization
    randomization_chance = max(0.3, 1 - confidence)
    
    if random.random() < randomization_chance:
        possible_moods = MOOD_RANDOMIZATION.get(detected_mood, [detected_mood])
        return random.choice(possible_moods)
    
    return detected_mood

@mood_router.post("/detect", response_model=MoodDetectionResponse)
async def detect_emotion(request: EmotionRequest):
    try:
        # Initialize emotion detector
        detector = EmotionDetector()
        
        # Detect emotion from image
        emotion_result = detector.detect_emotion(request.image)
        
        if not emotion_result:
            raise HTTPException(status_code=400, detail="No emotion detected in the image")
        
        # Randomize mood
        randomized_mood = randomize_mood(emotion_result['emotion'], emotion_result['confidence'])
        
        # Get music recommendations based on emotion
        recommendations = await fetch_random_tracks(
            mood=randomized_mood,
            limit=10,
            language=request.language
        )
        
        # Combine results
        return {
            "emotion": randomized_mood,
            "confidence": emotion_result['confidence'],
            "playlist": recommendations
        }
        
    except Exception as e:
        logger.error(f"Error detecting emotion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@mood_router.post("/text/analyze")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text sentiment and return music recommendations.
    
    Args:
        request (TextAnalysisRequest): Request containing text and options
        
    Returns:
        dict: Contains sentiment scores, detected mood, and music recommendations
    """
    try:
        # Initialize text sentiment analyzer
        analyzer = TextSentimentAnalyzer()
        
        # Validate language
        normalized_lang = validate_language(request.language)
        
        # Analyze text sentiment
        sentiment_result = analyzer.analyze_text(request.text)
        
        # Get music recommendations based on detected mood
        recommendations = await fetch_random_tracks(
            mood=sentiment_result['mood'],
            limit=request.limit,
            language=normalized_lang
        )
        
        # Combine results
        return {
            'sentiment_scores': sentiment_result['sentiment_scores'],
            'mood': sentiment_result['mood'],
            'recommendations': recommendations
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text sentiment: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@mood_router.get("/languages")
async def get_languages():
    """Get list of supported languages for recommendations."""
    try:
        from ..services.spotify_service import get_supported_languages
        return get_supported_languages()
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@mood_router.get("/emotions")
async def get_supported_mood_emotions():
    """
    Return list of supported emotions
    """
    return get_supported_emotions()

@mood_router.get("/playlist", response_model=List[SpotifyTrack])
async def get_mood_playlist(
    mood: str, 
    limit: int = 10
):
    """
    Generate a playlist based on detected mood
    """
    try:
        recommendations = await fetch_random_tracks(
            mood=mood,
            limit=limit,
            language=None
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playlist generation error: {str(e)}")

def capture_webcam_image(timeout: int = 5) -> np.ndarray:
    """
    Capture an image from the default webcam.
    
    Args:
        timeout (int, optional): Maximum time to wait for a valid image. Defaults to 5 seconds.
    
    Returns:
        np.ndarray: Captured image as a NumPy array
    """
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Could not open webcam")
        raise HTTPException(status_code=500, detail="Could not access webcam")
    
    try:
        # Give the camera some time to warm up
        for _ in range(timeout * 10):  # 10 attempts per second
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if ret:
                # Validate the captured image
                try:
                    result = EmotionDetector().detect_emotion(frame)
                    logger.debug("Successfully captured webcam image")
                    return frame
                except ValueError as val_error:
                    logger.warning(f"Captured invalid image: {val_error}")
            
            # Small delay between captures
            cv2.waitKey(100)
        
        # If no valid image was captured
        logger.error("Failed to capture a valid image from webcam")
        raise HTTPException(status_code=500, detail="Could not capture a valid image")
    
    finally:
        # Always release the capture
        cap.release()

@mood_router.post("/detect-webcam", response_model=MoodDetectionResponse)
async def detect_mood_from_webcam():
    """
    Detect emotion from a webcam-captured image
    """
    try:
        # Capture image from webcam
        image_np = capture_webcam_image()
        
        # Detect emotion
        emotion_result = EmotionDetector().detect_emotion(image_np)
        
        if not emotion_result:
            raise HTTPException(status_code=400, detail="No emotion detected in the image")
        
        # Randomize mood
        randomized_mood = randomize_mood(emotion_result['emotion'], emotion_result['confidence'])
        
        # Get music recommendations based on emotion
        recommendations = await fetch_random_tracks(
            mood=randomized_mood,
            limit=10,
            language=None
        )
        
        # Combine results
        return {
            "emotion": randomized_mood,
            "confidence": emotion_result['confidence'],
            "playlist": recommendations
        }
        
    except Exception as e:
        logger.error(f"Unexpected error in mood detection: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
