import sys
from unittest.mock import MagicMock

# Mock spotipy before importing the service
mock_spotipy = MagicMock()
sys.modules['spotipy'] = mock_spotipy
sys.modules['spotipy.oauth2'] = MagicMock()

from src.services.spotify_service import get_supported_languages, validate_language

def test_get_supported_languages():
    languages = get_supported_languages()
    assert isinstance(languages, list)
    assert 'english' in languages
    assert 'hindi' in languages
    assert 'bangla' in languages
    assert 'korean' in languages
    assert 'spanish' in languages
    assert 'japanese' in languages
    assert 'french' in languages
    assert 'portuguese' in languages
    assert len(languages) == 8

def test_validate_language_exact_match():
    assert validate_language('english') == 'english'
    assert validate_language('Hindi') == 'hindi'
    assert validate_language('BANGLA') == 'bangla'

def test_validate_language_code_mapping():
    assert validate_language('en') == 'english'
    assert validate_language('hi') == 'hindi'
    assert validate_language('bn') == 'bangla'
    assert validate_language('kor') == 'korean'
    assert validate_language('es') == 'spanish'
    assert validate_language('ja') == 'japanese'
    assert validate_language('fr') == 'french'
    assert validate_language('pt') == 'portuguese'

def test_validate_language_none():
    assert validate_language(None) is None

def test_validate_language_unsupported():
    assert validate_language('german') is None
    assert validate_language('de') is None
    assert validate_language('') is None
