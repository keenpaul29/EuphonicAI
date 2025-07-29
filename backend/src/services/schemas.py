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
    artists: List[SpotifyArtist] = Field(..., description="List of artists")
    mood: Optional[str] = Field(None, description="Mood associated with the track")
    image_url: Optional[str] = Field(None, description="URL of the track's album artwork")
    preview_url: Optional[str] = Field(None, description="URL for 30-second preview")
    uri: str = Field(..., description="Spotify URI for the track")
    
    @property
    def artist(self) -> str:
        """
        Get the primary artist name
        """
        return self.artists[0].name if self.artists else "Unknown"
    
    class Config:
        """
        Pydantic configuration for SpotifyTrack
        """
        schema_extra = {
            "example": {
                "id": "5H0Yfo3acNXU278LqN47pA",
                "name": "Happy B'Day",
                "artists": [{"id": "0TnOYISbd1XYRBk9myaseg", "name": "D Soldierz"}],
                "mood": "happy",
                "image_url": "https://i.scdn.co/image/ab67616d00001e02...",
                "preview_url": "https://p.scdn.co/mp3-preview/...",
                "uri": "spotify:track:5H0Yfo3acNXU278LqN47pA"
            }
        }
        
# Export the schemas
__all__ = ['SpotifyArtist', 'SpotifyTrack']
