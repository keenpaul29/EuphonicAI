from fastapi import APIRouter, HTTPException
from typing import List, Optional

# Spotify Service
from ..services.spotify_service import (
    generate_mood_playlist, 
    search_tracks,
    fetch_random_tracks,
    get_spotify_client
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
    limit: Optional[int] = 10,
    language: Optional[str] = None
):
    """
    Search Spotify tracks with optional mood filtering
    """
    try:
        tracks = search_tracks(query, limit, language=language)
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
        tracks = await fetch_random_tracks(mood, limit)
        return tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Random tracks error: {str(e)}")

@spotify_router.get("/tracks", response_model=List[SpotifyTrack])
async def get_tracks_by_ids(ids: str):
    """
    Fetch track details for a comma-separated list of Spotify track IDs.
    """
    try:
        client = get_spotify_client()
        if not client:
            raise HTTPException(status_code=500, detail="Spotify client not available")
        id_list = [tid.strip() for tid in ids.split(',') if tid.strip()]
        results = client.tracks(id_list)
        tracks: List[SpotifyTrack] = []
        for item in results.get('tracks', []):
            album_art_url = None
            images = item.get('album', {}).get('images', [])
            if images:
                album_art_url = images[0]['url']
            track = SpotifyTrack(
                id=item['id'],
                name=item['name'],
                artist=item['artists'][0]['name'] if item['artists'] else "Unknown",
                artists=[{'id': a.get('id', 'unknown'), 'name': a['name']} for a in item['artists']] if item['artists'] else None,
                album_name=item.get('album', {}).get('name'),
                album_art_url=album_art_url,
                preview_url=item.get('preview_url'),
                external_url=item.get('external_urls', {}).get('spotify'),
                uri=item['uri'],
                mood='unknown'
            )
            tracks.append(track)
        return tracks
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tracks fetch error: {str(e)}")
