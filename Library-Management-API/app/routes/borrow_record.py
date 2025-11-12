from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from typing import List

from app.config.database import get_db
from app.models.borrow_record import BorrowRecord as BorrowRecordModel
from app.models.book import Book as BookModel
from app.schemas.borrow_record import (
    BorrowRecordCreate,
    BorrowRecordUpdate,
    BorrowRecordResponse,
    MessageResponse,
)

router = APIRouter(prefix="/borrow-records", tags=["Borrow Records"])

# ----------------------
# CRUD Endpoints
# ----------------------
# Get all borrower records (with pagination)
@router.get("/", response_model=List[BorrowRecordResponse])
def get_all_borrow_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    records = db.query(BorrowRecordModel).offset(skip).limit(limit).all()
    if not records:
        raise HTTPException(status_code=404, detail="No borrow records found")
    return records

# Get borrower record by ID
@router.get("/{record_id}", response_model=BorrowRecordResponse)
def get_borrow_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(BorrowRecordModel).filter(BorrowRecordModel.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return record

# Create a new borrower record
@router.post("/", response_model=BorrowRecordResponse)
def create_borrow_record(record: BorrowRecordCreate, db: Session = Depends(get_db)):
    # Validate book exists
    book = db.query(BookModel).filter(BookModel.id == record.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        db_record = BorrowRecordModel(**record.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Borrow record already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error")
    
# Update a borrower record
@router.put("/{record_id}", response_model=BorrowRecordResponse)
def update_borrow_record(record_id: int, record: BorrowRecordUpdate, db: Session = Depends(get_db)):
    db_record = db.query(BorrowRecordModel).filter(BorrowRecordModel.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    try:
        for key, value in record.model_dump(exclude_unset=True).items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update borrow record")

# Delete a borrower record
@router.delete("/{record_id}", response_model=MessageResponse)
def delete_borrow_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(BorrowRecordModel).filter(BorrowRecordModel.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    try:
        db.delete(db_record)
        db.commit()
        return {"message": "Borrow record deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete borrow record")

# ----------------------
# Filter / Search Endpoints
# ----------------------
# Search by borrower name, book title, author name, genre name, publication year