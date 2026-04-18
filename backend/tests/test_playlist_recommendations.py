import pytest
import sys
import asyncio
from unittest.mock import MagicMock, patch

# Mock spotipy before importing the service
mock_spotipy = MagicMock()
sys.modules['spotipy'] = mock_spotipy
sys.modules['spotipy.oauth2'] = MagicMock()

from src.services.spotify_service import fetch_mood_playlists, generate_mock_playlists, SpotifyPlaylist

def test_generate_mock_playlists():
    playlists = generate_mock_playlists('happy', limit=3)
    assert len(playlists) == 3
    assert all(isinstance(p, SpotifyPlaylist) for p in playlists)
    assert all('happy' in p.name.lower() or (p.description and 'happy' in p.description.lower()) for p in playlists)
    assert playlists[0].id == 'mock_pl_happy_0'

def test_fetch_mood_playlists_no_client():
    # Test fallback to mock when client is not available
    with patch('src.services.spotify_service.get_spotify_client', return_value=None):
        playlists = asyncio.run(fetch_mood_playlists('sad', limit=2))
        assert len(playlists) == 2
        assert all('sad' in p.name.lower() or (p.description and 'sad' in p.description.lower()) for p in playlists)
        assert playlists[0].id.startswith('mock_pl_sad_')

def test_fetch_mood_playlists_with_client():
    # Mock Spotify client
    mock_client = MagicMock()
    mock_client.search.return_value = {
        'playlists': {
            'items': [
                {
                    'id': 'pl1',
                    'name': 'Real Playlist 1',
                    'description': 'Description 1',
                    'images': [{'url': 'http://image1.jpg'}],
                    'external_urls': {'spotify': 'http://spotify.com/pl1'},
                    'uri': 'spotify:playlist:pl1'
                }
            ]
        }
    }

    with patch('src.services.spotify_service.get_spotify_client', return_value=mock_client):
        playlists = asyncio.run(fetch_mood_playlists('happy', limit=1))
        assert len(playlists) == 1
        assert playlists[0].name == 'Real Playlist 1'
        assert playlists[0].id == 'pl1'
        assert playlists[0].image_url == 'http://image1.jpg'
        mock_client.search.assert_called_once()
