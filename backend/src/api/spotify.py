from fastapi import APIRouter, HTTPException
from typing import List, Optional

# Spotify Service
from ..services.spotify_service import (
    generate_mood_playlist, 
    search_tracks,
    fetch_random_tracks
)
from ..services.schemas import SpotifyTrack

spotify_router = APIRouter()

@spotify_router.get("/playlist/{mood}", response_model=List[SpotifyTrack])
async def get_mood_playlist(
    mood: str, 
    limit: Optional[int] = 10
):
    """
    Generate a Spotify playlist based on mood
    """
    try:
        playlist = await generate_mood_playlist(mood, limit)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playlist generation error: {str(e)}")

@spotify_router.get("/search", response_model=List[SpotifyTrack])
async def search_spotify_tracks(
    query: str, 
    mood: Optional[str] = None,
    limit: Optional[int] = 10
):
    """
    Search Spotify tracks with optional mood filtering
    """
    try:
        tracks = search_tracks(query, limit)
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Track search error: {str(e)}")

@spotify_router.get("/random-tracks", response_model=List[SpotifyTrack])
async def get_random_tracks(
    mood: str, 
    limit: Optional[int] = 10
):
    """
    Fetch random Spotify tracks based on mood
    """
    try:
        tracks = fetch_random_tracks(mood, limit)
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Random tracks error: {str(e)}")
