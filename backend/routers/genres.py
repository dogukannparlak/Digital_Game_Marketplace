"""
Genres Router - Public genre listing
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..auth_utils import get_db

router = APIRouter(
    prefix="/genres",
    tags=["genres"]
)

@router.get("/", response_model=List[schemas.Genre])
def list_genres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all available genres"""
    return db.query(models.Genre).offset(skip).limit(limit).all()

@router.get("/{genre_id}", response_model=schemas.Genre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """Get a specific genre by ID"""
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.get("/{genre_id}/games", response_model=List[schemas.GamePublic])
def get_games_by_genre(
    genre_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all approved games in a specific genre"""
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    games = db.query(models.Game).join(models.Game.genres).filter(
        models.Genre.id == genre_id,
        models.Game.status == models.GameStatus.APPROVED
    ).offset(skip).limit(limit).all()

    return games

@router.get("/slug/{slug}", response_model=schemas.Genre)
def get_genre_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get a specific genre by slug"""
    genre = db.query(models.Genre).filter(models.Genre.slug == slug).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre
