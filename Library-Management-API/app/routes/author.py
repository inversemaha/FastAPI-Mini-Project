from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.config.database import get_db
from app.models.author import Author as AuthorModel
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate, MessageResponse

router = APIRouter(prefix="/authors", tags=["Authors"])

# ----------------------
# CRUD Endpoints
# ----------------------

# Gel all authors (with pagination)
@router.get("/", response_model=list[AuthorResponse])
def get_all_authors(skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).offset(skip).limit(limit).all()
    if not author:
        raise HTTPException(status_code=404, detail="No authors found")
    return author

# Get author by ID
@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

# Create a new author
@router.post("/", response_model=AuthorResponse)
def create_autor(author:AuthorCreate, db: Session = Depends(get_db)):
    try:
        db_author = AuthorModel(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Author already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")

# Update an author
@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author:AuthorUpdate, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    try:
        for key, value in author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
        return db_author
    except Exception:
        raise HTTPException(status_code=500, detail="Failled to update author")

# Delete an author
@router.delete("/{author_id}", response_model=MessageResponse)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    try:
        db.delete(db_author)
        db.commit()
        return {"message": "Author deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to delete author")


# ----------------------
# Filter / Search Endpoints
# ----------------------
# Search by name and/or country