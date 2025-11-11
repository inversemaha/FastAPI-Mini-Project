from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_

from app.config.database import get_db
from app.models.book import Book as BookModel
from app.models.author import Author as AuthorModel
from app.models.genre import Genre as GenreModel
from app.schemas.book import BookCreate, BookUpdate, BookResponse, MessageResponse

router = APIRouter(prefix="/books", tags=["Books"])

# ----------------------
# CRUD Endpoints
# ----------------------
# Get all books (with pagination)
@router.get("/", response_model=list[BookResponse])
def get_all_books(skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    books = (db.query(BookModel)
             .options(joinedload(BookModel.author), joinedload(BookModel.genre))
             .offset(skip).limit(limit)
             .all()
             )
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

# Get a single book by ID (with relationships)
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = (db.query(BookModel)
            .options(joinedload(BookModel.author), joinedload(BookModel.genre))
            .filter(BookModel.id == book_id)
            .first()
            )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Create a new book
@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Validate author and genre before existence before creation
    author = db.query(AuthorModel).filter(AuthorModel.id == book.author_id).first()
    genre = db.query(GenreModel).filter(GenreModel.id == book.genre_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    try:
        db_book = BookModel(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")
    
# Update a book
@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    try:
        for key, value in book.model_dump(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update book")
    
# Delete a book
@router.delete("/{book_id}", response_model=MessageResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete book")

# ----------------------
# Filter / Search Endpoints
# ----------------------
# Filter by title, author_id, genre_id, and publication_year
# Global keyword search (title, author name, genre name)