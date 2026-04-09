from pydantic import BaseModel, Field
from typing import Optional, List

class SpotifyArtist(BaseModel):
    """
    Pydantic model representing a Spotify artist
    """
    id: str = Field(..., description="Spotify artist ID")
    name: str = Field(..., description="Artist name")
    
    class Config:
        """
        Pydantic configuration for SpotifyArtist
        """
        schema_extra = {
            "example": {
                "id": "0TnOYISbd1XYRBk9myaseg",
                "name": "Pitbull"
            }
        }

class SpotifyTrack(BaseModel):
    """
    Pydantic model representing a Spotify track
    """
    id: str = Field(..., description="Spotify track ID")
    name: str = Field(..., description="Track name")
    artist: str = Field(..., description="Primary artist name")
    artists: Optional[List[SpotifyArtist]] = Field(None, description="List of artists")
    album_name: Optional[str] = Field(None, description="Album name")
    album_art_url: Optional[str] = Field(None, description="URL of the track's album artwork")
    preview_url: Optional[str] = Field(None, description="URL for 30-second preview")
    external_url: Optional[str] = Field(None, description="Spotify external URL")
    uri: Optional[str] = Field(None, description="Spotify URI for the track")
    mood: Optional[str] = Field(None, description="Mood associated with the track")
    
    class Config:
        """
        Pydantic configuration for SpotifyTrack
        """
        schema_extra = {
            "example": {
                "id": "5H0Yfo3acNXU278LqN47pA",
                "name": "Happy B'Day",
                "artist": "D Soldierz",
                "album_name": "Party Hits",
                "album_art_url": "https://i.scdn.co/image/ab67616d00001e02...",
                "preview_url": "https://p.scdn.co/mp3-preview/...",
                "external_url": "https://open.spotify.com/track/...",
                "uri": "spotify:track:5H0Yfo3acNXU278LqN47pA",
                "mood": "happy"
            }
        }
        
# Export the schemas
__all__ = ['SpotifyArtist', 'SpotifyTrack']
