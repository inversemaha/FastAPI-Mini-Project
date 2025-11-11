from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from typing import List

from app.config.database import get_db
from app.models.genre import Genre as GenreModel
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse, MessageResponse

router = APIRouter(prefix="/genres", tags=["Genres"])

# ----------------------
# CRUD Endpoints
# ----------------------
# Get all genres (with pagination)
@router.get("/", response_model=List[GenreResponse])
def get_all_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    genres = db.query(GenreModel).offset(skip).limit(limit).all()
    if not genres:
        raise HTTPException(status_code=404, detail="No genres found")
    return genres


# Get genre by ID
@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(GenreModel).filter(GenreModel.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


# Create genre
@router.post("/", response_model=GenreResponse)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    try:
        db_genre = GenreModel(**genre.model_dump())
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Genre already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error")


# Update genre
@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, genre: GenreUpdate, db: Session = Depends(get_db)):
    db_genre = db.query(GenreModel).filter(GenreModel.id == genre_id).first()
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    try:
        for key, value in genre.model_dump(exclude_unset=True).items():
            setattr(db_genre, key, value)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update genre")


# Delete genre
@router.delete("/{genre_id}", response_model=MessageResponse)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = db.query(GenreModel).filter(GenreModel.id == genre_id).first()
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    try:
        db.delete(db_genre)
        db.commit()
        return {"message": "Genre deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete genre")

# ----------------------
# Filter / Search Endpoints
# ----------------------
# Filter by name (exact or partial match)
# Global keyword search