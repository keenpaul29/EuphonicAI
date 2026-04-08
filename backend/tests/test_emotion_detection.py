import pytest
import numpy as np
from src.services.emotion_detection import EmotionDetector, get_supported_emotions, decode_image

def test_get_supported_emotions():
    emotions = get_supported_emotions()
    assert isinstance(emotions, list)
    assert 'happy' in emotions
    assert 'sad' in emotions
    assert 'angry' in emotions
    assert 'neutral' in emotions

def test_decode_image_invalid():
    with pytest.raises(ValueError):
        decode_image("invalid_base64_string")

def test_emotion_detector_fallback():
    detector = EmotionDetector()
    # Pass a dummy zero array to simulate an image without a face
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)

    result = detector.detect_emotion(dummy_img)

    assert isinstance(result, dict)
    assert 'emotion' in result
    assert 'confidence' in result
    assert 'emotion_scores' in result
    # Expect the fallback behavior to return neutral
    assert result['emotion'] in ['neutral', 'angry']