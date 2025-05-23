from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import base64
import cv2
from src.services.emotion_detection import EmotionDetector, decode_image
from src.services.spotify_service import fetch_random_tracks, get_supported_languages as get_spotify_languages, SpotifyTrack, SpotifyArtist, get_spotify_client
import logging
import traceback

logger = logging.getLogger(__name__)

# Router for emotion-related endpoints
emotion_router = APIRouter()

# Pydantic model for image input
class EmotionDetectionRequest(BaseModel):
    image: str  # base64 encoded image
    language: str | None = None  # Optional language preference
    include_playlists: bool = False  # Optional flag to include playlist recommendations

# Pydantic model for artist response
class ArtistResponse(BaseModel):
    id: str
    name: str

# Pydantic model for track response
class TrackResponse(BaseModel):
    id: str
    name: str
    artists: list[ArtistResponse]
    mood: str
    uri: str
    image_url: str | None = None
    preview_url: str | None = None

# Pydantic model for playlist response
class PlaylistResponse(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    external_url: str
    tracks: list[TrackResponse]

# Pydantic model for emotion detection response
class EmotionDetectionResponse(BaseModel):
    emotion: str
    confidence: float
    emotion_scores: dict[str, float]
    playlist: list[TrackResponse]
    recommended_playlists: list[PlaylistResponse] | None = None
    
# Helper function to convert SpotifyTrack to TrackResponse
def convert_to_track_response(track: SpotifyTrack) -> TrackResponse:
    """
    Convert a SpotifyTrack named tuple to a TrackResponse Pydantic model.
    
    Args:
        track (SpotifyTrack): The track to convert
        
    Returns:
        TrackResponse: The converted track
    """
    return TrackResponse(
        id=track.id,
        name=track.name,
        artists=[ArtistResponse(id=artist.id, name=artist.name) for artist in track.artists],
        mood=track.mood,
        uri=track.uri,
        image_url=track.image_url,
        preview_url=track.preview_url
    )

def validate_language(language: str | None) -> str | None:
    """
    Validate and normalize language input.
    
    Args:
        language (str | None): Input language string
        
    Returns:
        str | None: Normalized language code or None if not supported/provided
    """
    if not language:
        return None
        
    try:
        languages = get_spotify_languages()
        language = language.lower()
        
        # Direct match
        if language in languages:
            return language
            
        # Handle common language codes
        language_map = {
            'en': 'english',
            'hi': 'hindi',
            'bn': 'bangla',
            'ko': 'korean',
            'es': 'spanish',
            'ja': 'japanese',
            'fr': 'french',
            'pt': 'portuguese'
        }
        
        if language in language_map:
            mapped_lang = language_map[language]
            if mapped_lang in languages:
                return mapped_lang
                
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported languages: {', '.join(languages)}"
        )
    except Exception as e:
        logger.error(f"Error validating language: {str(e)}")
        return None

@emotion_router.post("/detect", response_model=EmotionDetectionResponse)
async def detect_emotion_endpoint(request: EmotionDetectionRequest):
    """
    Detect emotion from base64 encoded image and optionally return playlist recommendations.
    
    Args:
        request (EmotionDetectionRequest): Request containing base64 encoded image and options
        
    Returns:
        EmotionDetectionResponse: Detected emotion and optional playlist recommendations
    """
    try:
        logger.info("Starting emotion detection request")
        
        # Validate language
        language = validate_language(request.language)
        logger.info(f"Validated language: {language}")
        
        # Initialize emotion detector
        detector = EmotionDetector()
        logger.info("Initialized emotion detector")
        
        # Detect emotion
        try:
            # Decode image
            try:
                logger.info("Starting image decoding")
                image_array = decode_image(request.image)
                if image_array is None:
                    logger.error("Image decoding returned None")
                    raise HTTPException(status_code=400, detail="Invalid image data")
                logger.info(f"Successfully decoded image with shape: {image_array.shape}")
            except ValueError as e:
                logger.error(f"Error decoding image: {e}")
                raise HTTPException(status_code=400, detail=str(e))
            
            # Detect emotion using the detector
            logger.info("Starting emotion detection")
            emotion_result = detector.detect_emotion(image_array)
            if not emotion_result:
                logger.error("Could not detect face or analyze emotions. Please ensure your face is clearly visible, well-lit, and looking at the camera.")
                raise HTTPException(
                    status_code=400,
                    detail="Could not detect face or analyze emotions. Please ensure your face is clearly visible, well-lit, and looking at the camera."
                )
            logger.info(f"Detected emotion: {emotion_result}")
            
            # Get playlist recommendations
            playlist = []
            recommended_playlists = None
            
            if request.include_playlists:
                logger.info("Attempting to get playlist recommendations")
                try:
                    # First check if Spotify is available
                    spotify = get_spotify_client()
                    if spotify:
                        logger.info("Successfully got Spotify client")
                        # Get tracks for detected emotion
                        playlist = await fetch_random_tracks(
                            mood=emotion_result['emotion'],
                            limit=10,
                            language=language
                        )
                        logger.info(f"Got {len(playlist)} tracks for playlist")
                        
                        # TODO: Implement playlist recommendations
                    else:
                        logger.warning("Spotify client is not available, skipping playlist recommendations")
                except Exception as e:
                    logger.error(f"Error with Spotify service: {str(e)}")
                    logger.error(traceback.format_exc())
                    # Continue without playlist recommendations
                    playlist = []
            
            # Convert SpotifyTrack objects to TrackResponse objects
            track_responses = []
            try:
                if playlist:
                    logger.info(f"Converting {len(playlist)} tracks to TrackResponse objects")
                    track_responses = [convert_to_track_response(track) for track in playlist]
                    logger.info(f"Successfully converted {len(track_responses)} tracks")
            except Exception as e:
                logger.error(f"Error converting tracks: {e}")
                logger.error(traceback.format_exc())
                track_responses = []
            
            # Prepare response
            logger.info("Preparing response")
            return EmotionDetectionResponse(
                emotion=emotion_result['emotion'],
                confidence=emotion_result['confidence'],
                emotion_scores=emotion_result['emotion_scores'],
                playlist=track_responses,
                recommended_playlists=recommended_playlists
            )
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in emotion detection endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@emotion_router.get("/languages")
async def get_supported_languages_endpoint():
    """
    Get list of supported languages for song recommendations
    
    Returns:
        List[str]: List of supported language codes
    """
    try:
        return get_spotify_languages()
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error getting supported languages")
