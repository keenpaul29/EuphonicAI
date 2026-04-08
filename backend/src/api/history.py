from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db, HistoryEntry

history_router = APIRouter()

class TrackSchema(BaseModel):
    id: str
    name: str
    artist: str
    album_art_url: Optional[str] = None
    preview_url: Optional[str] = None
    external_url: Optional[str] = None

class HistoryCreateSchema(BaseModel):
    mood: str
    confidence: Optional[float] = None
    tracks: List[dict] # Accepting dicts for flexibility

class HistoryResponseSchema(BaseModel):
    id: int
    user_id: str
    mood: str
    confidence: Optional[float] = None
    tracks: List[dict]
    created_at: datetime

    class Config:
        orm_mode = True

def get_user_id_from_header(authorization: Optional[str] = Header(None)) -> str:
    # In a real app we would verify the Clerk JWT here
    # For now, we will extract a mock user ID or "anonymous"
    if not authorization or not authorization.startswith("Bearer "):
        return "anonymous"
    # Using the raw token as the mock user_id for demonstration
    return authorization.split(" ")[1][:50]

@history_router.post("/", response_model=HistoryResponseSchema)
def add_history_entry(
    entry: HistoryCreateSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header)
):
    db_entry = HistoryEntry(
        user_id=user_id,
        mood=entry.mood,
        confidence=entry.confidence,
        tracks=entry.tracks
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@history_router.get("/", response_model=List[HistoryResponseSchema])
def get_history(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header),
    limit: int = 50
):
    entries = db.query(HistoryEntry).filter(HistoryEntry.user_id == user_id).order_by(HistoryEntry.created_at.desc()).limit(limit).all()
    return entries

@history_router.delete("/{entry_id}")
def delete_history_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header)
):
    entry = db.query(HistoryEntry).filter(HistoryEntry.id == entry_id, HistoryEntry.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted"}

@history_router.delete("/")
def clear_history(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_user_id_from_header)
):
    db.query(HistoryEntry).filter(HistoryEntry.user_id == user_id).delete()
    db.commit()
    return {"message": "History cleared"}
