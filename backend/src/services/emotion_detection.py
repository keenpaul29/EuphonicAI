import numpy as np
import logging
import traceback
import cv2
import sys
import base64
import io
from PIL import Image
from typing import Dict, Optional, Union
from deepface import DeepFace

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class EmotionDetector:
    def __init__(self):
        pass
        
    def detect_emotion(self, image_array: np.ndarray) -> Dict[str, Union[str, float, Dict[str, float]]]:
        """
        Detect emotion from image array using DeepFace.
        
        Args:
            image_array (np.ndarray): Image as NumPy array
            
        Returns:
            dict: Contains emotion, confidence score, and emotion scores
        """
        try:
            logger.debug(f"Input image array shape: {image_array.shape}, dtype: {image_array.dtype}")
            
            # Save debug image
            debug_path = "debug_input.png"
            Image.fromarray(image_array).save(debug_path)
            logger.debug(f"Saved input image to {debug_path}")
            
            # Use DeepFace for emotion detection with fallback
            try:
                # First try with enforce_detection=False to be more lenient
                result = DeepFace.analyze(
                    image_array,
                    actions=['emotion'],
                    enforce_detection=False,  # More lenient face detection
                    detector_backend='opencv'  # Use OpenCV for faster detection
                )
                
                if not result or not isinstance(result, list) or len(result) == 0:
                    logger.warning("DeepFace returned no results with lenient detection, trying with different backend")
                    # Try with a different detector backend
                    result = DeepFace.analyze(
                        image_array,
                        actions=['emotion'],
                        enforce_detection=False,
                        detector_backend='retinaface'  # Try alternative face detector
                    )
                
                if not result or not isinstance(result, list) or len(result) == 0:
                    logger.warning("DeepFace returned no results with all detection methods")
                    # Return a neutral fallback when detection fails
                    return {
                        'emotion': 'neutral',
                        'confidence': 0.5,
                        'emotion_scores': {
                            'angry': 0.05, 'disgust': 0.05, 'fear': 0.05, 
                            'happy': 0.1, 'sad': 0.1, 'surprise': 0.05, 
                            'neutral': 0.6
                        }
                    }
                    
                # Get the first face result
                face_result = result[0]
                logger.info(f"DeepFace analysis result: {face_result}")
                
                # Extract emotion scores
                emotion_scores = face_result.get('emotion', {})
                if not emotion_scores:
                    logger.warning("No emotion scores in DeepFace result, using fallback")
                    return {
                        'emotion': 'neutral',
                        'confidence': 0.5,
                        'emotion_scores': {
                            'angry': 0.05, 'disgust': 0.05, 'fear': 0.05, 
                            'happy': 0.1, 'sad': 0.1, 'surprise': 0.05, 
                            'neutral': 0.6
                        }
                    }
                    
                # Find the dominant emotion
                dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                
                # Normalize emotion names to match our supported list
                emotion_name = dominant_emotion[0].lower()
                # Map 'disgust' to 'disgusted', etc. to match spotify_service.py mood names
                emotion_map = {
                    'disgust': 'disgusted',
                    'fear': 'fearful',
                    'surprise': 'surprised'
                }
                emotion_name = emotion_map.get(emotion_name, emotion_name)
                
                return {
                    'emotion': emotion_name,
                    'confidence': dominant_emotion[1] / 100.0,  # Convert percentage to decimal
                    'emotion_scores': {k.lower(): v/100.0 for k, v in emotion_scores.items()}
                }
                
            except Exception as e:
                logger.error(f"DeepFace analysis failed: {str(e)}")
                logger.error(traceback.format_exc())
                # Return a fallback emotion rather than None
                return {
                    'emotion': 'neutral',
                    'confidence': 0.5,
                    'emotion_scores': {
                        'angry': 0.05, 'disgust': 0.05, 'fear': 0.05, 
                        'happy': 0.1, 'sad': 0.1, 'surprise': 0.05, 
                        'neutral': 0.6
                    }
                }
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            logger.error(traceback.format_exc())
            # Return a fallback emotion rather than None
            return {
                'emotion': 'neutral',
                'confidence': 0.5,
                'emotion_scores': {
                    'angry': 0.05, 'disgust': 0.05, 'fear': 0.05, 
                    'happy': 0.1, 'sad': 0.1, 'surprise': 0.05, 
                    'neutral': 0.6
                }
            }

def decode_image(image_str: str) -> np.ndarray:
    """
    Decode base64 image string to NumPy array.
    
    Args:
        image_str (str): Base64 encoded image string
    
    Returns:
        np.ndarray: Decoded image as NumPy array
    """
    try:
        # Log input format
        logger.debug(f"Image string starts with: {image_str[:50]}...")
        
        # Handle data URL format
        if ',' in image_str:
            logger.debug("Found data URL format, splitting at comma")
            image_str = image_str.split(',')[1]
        
        # Decode base64 string
        try:
            image_data = base64.b64decode(image_str)
            logger.debug(f"Successfully decoded base64 data, size: {len(image_data)} bytes")
        except Exception as e:
            logger.error(f"Base64 decoding failed: {e}")
            raise ValueError("Invalid base64 data")
        
        # Convert to PIL Image
        try:
            image = Image.open(io.BytesIO(image_data))
            logger.debug(f"Successfully opened image: format={image.format}, size={image.size}, mode={image.mode}")
        except Exception as e:
            logger.error(f"Failed to open image data: {e}")
            raise ValueError("Invalid image format")
        
        # Convert to RGB if needed and ensure proper size
        if image.mode != 'RGB':
            logger.debug(f"Converting image from {image.mode} to RGB")
            image = image.convert('RGB')
        
        # Save original image for debugging
        debug_path = "debug_original.png"
        image.save(debug_path)
        logger.debug(f"Saved original image to {debug_path}")
        
        # Ensure minimum size for face detection
        min_dimension = 480
        if min(image.size) < min_dimension:
            ratio = min_dimension / min(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            logger.debug(f"Upscaling image from {image.size} to {new_size}")
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Resize if image is too large
        max_dimension = 1024
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            logger.debug(f"Downscaling image from {image.size} to {new_size}")
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to NumPy array
        image_array = np.array(image)
        logger.debug(f"Converted to NumPy array with shape: {image_array.shape}, dtype: {image_array.dtype}")
        
        # Save processed image for debugging
        debug_path = "debug_processed.png"
        Image.fromarray(image_array).save(debug_path)
        logger.debug(f"Saved processed image to {debug_path}")
        
        return image_array
    
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        logger.error(traceback.format_exc())
        raise ValueError("Invalid image format")

def get_supported_emotions() -> list:
    """
    Return list of supported emotions.
    
    Returns:
        list: List of supported emotion categories
    """
    return ['happy', 'sad', 'neutral', 'angry', 'surprised', 'fearful', 'disgusted']
