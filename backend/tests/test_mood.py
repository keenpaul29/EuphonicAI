import pytest
import sys
import random
from unittest.mock import MagicMock, patch

# Provide stable mocks for dependencies needed for importing src.api.mood
@pytest.fixture(autouse=True, scope="module")
def mock_env_dependencies():
    with patch.dict('sys.modules', {
        'fastapi': MagicMock(),
        'pydantic': MagicMock(),
        'cv2': MagicMock(),
        'numpy': MagicMock(),
        'src.services.emotion_detection': MagicMock(),
        'src.services.text_sentiment': MagicMock(),
        'src.services.spotify_service': MagicMock(),
    }):
        yield

def test_randomize_mood_high_confidence():
    from src.api.mood import randomize_mood
    with patch('random.random', return_value=0.5):
        # confidence 1.0 -> randomization_chance = 0.3
        # 0.5 < 0.3 is False -> return original
        assert randomize_mood('happy', 1.0) == 'happy'

def test_randomize_mood_low_confidence_randomized():
    from src.api.mood import randomize_mood
    with patch('random.random', return_value=0.1):
        # confidence 0.1 -> randomization_chance = 0.9
        # 0.1 < 0.9 is True -> randomize
        # Uses 'random.choice'
        with patch('random.choice', return_value='surprise'):
            assert randomize_mood('happy', 0.1) == 'surprise'

def test_randomize_mood_low_confidence_not_randomized():
    from src.api.mood import randomize_mood
    with patch('random.random', return_value=0.95):
        # confidence 0.1 -> randomization_chance = 0.9
        # 0.95 < 0.9 is False -> return original
        assert randomize_mood('happy', 0.1) == 'happy'

def test_randomize_mood_unsupported_mood():
    from src.api.mood import randomize_mood
    with patch('random.random', return_value=0.1):
        # randomization_chance for 0.1 is 0.9. 0.1 < 0.9 -> True.
        # But 'unknown' not in MOOD_RANDOMIZATION, defaults to ['unknown']
        assert randomize_mood('unknown', 0.1) == 'unknown'

def test_all_moods_in_strategy():
    from src.api.mood import randomize_mood, MOOD_RANDOMIZATION
    for mood, expected_options in MOOD_RANDOMIZATION.items():
        with patch('random.random', return_value=0.0): # Force randomization
            # If we roll 0.0, it should pick one of the options
            randomized = randomize_mood(mood, 0.5)
            assert randomized in expected_options
