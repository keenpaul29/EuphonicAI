import logging
import traceback
import asyncio
from .celery_app import celery_app
from .services.emotion_detection import EmotionDetector, decode_image

logger = logging.getLogger(__name__)

# Load the detector once per worker process to save initialization time
_detector = None

def get_detector():
    global _detector
    if _detector is None:
        _detector = EmotionDetector()
    return _detector

@celery_app.task(name="tasks.detect_emotion")
def detect_emotion_task(image_base64: str) -> dict:
    """
    Celery task to detect emotion from a base64 image in the background.
    Returns the emotion detection result dict.
    """
    try:
        logger.info("Starting background emotion detection task")
        image_array = decode_image(image_base64)

        detector = get_detector()
        emotion_result = detector.detect_emotion(image_array)

        if not emotion_result:
            logger.warning("Emotion detection returned None, using default neutral")
            emotion_result = {
                'emotion': 'neutral',
                'confidence': 0.5,
                'emotion_scores': {
                    'angry': 0.05, 'disgust': 0.05, 'fear': 0.05,
                    'happy': 0.1, 'sad': 0.1, 'surprise': 0.05,
                    'neutral': 0.6
                }
            }

        return emotion_result

    except ValueError as e:
        logger.error(f"Image decoding failed in task: {e}")
        return {"error": "Invalid image format"}
    except Exception as e:
        logger.error(f"Background task error detecting emotion: {e}")
        logger.error(traceback.format_exc())
        return {"error": "Internal processing error"}
