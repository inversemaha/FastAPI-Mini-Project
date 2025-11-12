from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from typing import List

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
@router.get("/", response_model=List[BookResponse])
def get_all_books(skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    books = (db.query(BookModel)
             .options(joinedload(BookModel.author), joinedload(BookModel.genre))
             .offset(skip).limit(limit)
             .all())
    if not books:        
        raise HTTPException(status_code=404, detail="No books found")
    return books

# Get a single book by ID (with relationships)
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = (db.query(BookModel)
            .options(joinedload(BookModel.author), 
                    joinedload(BookModel.genre),
                    joinedload(BookModel.borrow_records))
            .filter(BookModel.id == book_id)
            .first()
            )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Manual serialization to prevent recursion
    return {
        "id": book.id,
        "title": book.title,
        "author_id": book.author_id,
        "genre_id": book.genre_id,
        "publication_year": book.publication_year,
        "author": book.author,
        "genre": book.genre,
        "borrow_records": [
            {
                "id": record.id,
                "book_id": record.book_id,
                "borrower_name": record.borrower_name,
                "borrow_date": record.borrow_date,
                "return_date": record.return_date,
                "book": None  # Prevent recursion
            }
            for record in book.borrow_records
        ]
    }

# Create a new book
@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Validate author and genre existence before creation
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
        
        # Load relationships for response and prevent recursion
        db_book = (db.query(BookModel)
                  .options(joinedload(BookModel.author), 
                          joinedload(BookModel.genre),
                          joinedload(BookModel.borrow_records))
                  .filter(BookModel.id == db_book.id)
                  .first())
        
        return {
            "id": db_book.id,
            "title": db_book.title,
            "author_id": db_book.author_id,
            "genre_id": db_book.genre_id,
            "publication_year": db_book.publication_year,
            "author": db_book.author,
            "genre": db_book.genre,
            "borrow_records": []  # New book has no borrows yet
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book already exists")
    except Exception:
        db.rollback()
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
        
        # Load relationships for response and prevent recursion
        db_book = (db.query(BookModel)
                  .options(joinedload(BookModel.author), 
                          joinedload(BookModel.genre),
                          joinedload(BookModel.borrow_records))
                  .filter(BookModel.id == book_id)
                  .first())
        
        return {
            "id": db_book.id,
            "title": db_book.title,
            "author_id": db_book.author_id,
            "genre_id": db_book.genre_id,
            "publication_year": db_book.publication_year,
            "author": db_book.author,
            "genre": db_book.genre,
            "borrow_records": [
                {
                    "id": record.id,
                    "book_id": record.book_id,
                    "borrower_name": record.borrower_name,
                    "borrow_date": record.borrow_date,
                    "return_date": record.return_date,
                    "book": None  # Prevent recursion
                }
                for record in db_book.borrow_records
            ]
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update book")
    
# Delete a book
@router.delete("/{book_id}", response_model=MessageResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    from app.models.borrow_record import BorrowRecord as BorrowRecordModel
    
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if book has any unreturned borrow records using direct query
    active_borrows = (db.query(BorrowRecordModel)
                     .filter(BorrowRecordModel.book_id == book_id)
                     .filter(BorrowRecordModel.return_date.is_(None))
                     .all())
    
    if active_borrows:
        borrower_names = [record.borrower_name for record in active_borrows]
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete book. Currently borrowed by: {', '.join(borrower_names)}"
        )
    
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