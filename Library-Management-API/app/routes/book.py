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
    from app.models.borrow_record import BorrowRecord as BorrowRecordModel
    
    books = (db.query(BookModel)
             .options(joinedload(BookModel.author), joinedload(BookModel.genre))
             .offset(skip).limit(limit)
             .all())
    if not books:        
        raise HTTPException(status_code=404, detail="No books found")
    
    # Calculate available copies for each book
    result = []
    for book in books:
        # Count active borrows (unreturned books)
        active_borrows_count = (db.query(BorrowRecordModel)
                               .filter(BorrowRecordModel.book_id == book.id)
                               .filter(BorrowRecordModel.return_date.is_(None))
                               .count())
        
        available_copies = book.total_copies - active_borrows_count
        
        book_data = {
            "id": book.id,
            "title": book.title,
            "author_id": book.author_id,
            "genre_id": book.genre_id,
            "publication_year": book.publication_year,
            "total_copies": book.total_copies,
            "author": book.author,
            "genre": book.genre,
            "available_copies": available_copies,
            "is_available": available_copies > 0
        }
        result.append(book_data)
    
    return result

# Get a single book by ID (with relationships)
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    from app.models.borrow_record import BorrowRecord as BorrowRecordModel
    
    book = (db.query(BookModel)
            .options(joinedload(BookModel.author), joinedload(BookModel.genre))
            .filter(BookModel.id == book_id)
            .first()
            )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Calculate available copies
    active_borrows_count = (db.query(BorrowRecordModel)
                           .filter(BorrowRecordModel.book_id == book_id)
                           .filter(BorrowRecordModel.return_date.is_(None))
                           .count())
    
    available_copies = book.total_copies - active_borrows_count
    
    return {
        "id": book.id,
        "title": book.title,
        "author_id": book.author_id,
        "genre_id": book.genre_id,
        "publication_year": book.publication_year,
        "total_copies": book.total_copies,
        "author": book.author,
        "genre": book.genre,
        "available_copies": available_copies,
        "is_available": available_copies > 0
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
        
        # Load relationships for response
        db_book = (db.query(BookModel)
                  .options(joinedload(BookModel.author), joinedload(BookModel.genre))
                  .filter(BookModel.id == db_book.id)
                  .first())
        
        return {
            "id": db_book.id,
            "title": db_book.title,
            "author_id": db_book.author_id,
            "genre_id": db_book.genre_id,
            "publication_year": db_book.publication_year,
            "total_copies": db_book.total_copies,
            "author": db_book.author,
            "genre": db_book.genre,
            "available_copies": db_book.total_copies,  # New book, all copies available
            "is_available": True
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
        
        # Load relationships and calculate availability
        from app.models.borrow_record import BorrowRecord as BorrowRecordModel
        
        db_book = (db.query(BookModel)
                  .options(joinedload(BookModel.author), joinedload(BookModel.genre))
                  .filter(BookModel.id == book_id)
                  .first())
        
        active_borrows_count = (db.query(BorrowRecordModel)
                               .filter(BorrowRecordModel.book_id == book_id)
                               .filter(BorrowRecordModel.return_date.is_(None))
                               .count())
        
        available_copies = db_book.total_copies - active_borrows_count
        
        return {
            "id": db_book.id,
            "title": db_book.title,
            "author_id": db_book.author_id,
            "genre_id": db_book.genre_id,
            "publication_year": db_book.publication_year,
            "total_copies": db_book.total_copies,
            "author": db_book.author,
            "genre": db_book.genre,
            "available_copies": available_copies,
            "is_available": available_copies > 0
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