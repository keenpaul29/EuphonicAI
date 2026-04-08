import pytest
from src.services.spotify_service import get_supported_languages, validate_language, generate_mock_tracks

def test_get_supported_languages():
    languages = get_supported_languages()
    assert isinstance(languages, list)
    assert 'english' in languages
    assert 'spanish' in languages

def test_validate_language_valid():
    assert validate_language('english') == 'english'
    assert validate_language('es') == 'spanish'
    assert validate_language('hin') == 'hindi'

def test_validate_language_invalid():
    assert validate_language('not_a_language') is None
    assert validate_language(None) is None

def test_generate_mock_tracks():
    limit = 5
    tracks = generate_mock_tracks('happy', limit)

    assert len(tracks) == limit
    assert tracks[0].mood == 'happy'
    assert "mock_happy_" in tracks[0].id