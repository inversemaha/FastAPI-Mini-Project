from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

# Type Checking for circular Relationship issue
if TYPE_CHECKING:
    from .book import BookResponse

#Base Schema
class BorrowRecordBase(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: Optional[datetime] = None

#Create Schema
class BorrowRecordCreate(BorrowRecordBase):
    pass

#Update Schema
class BorrowRecordUpdate(BaseModel):
    book_id: Optional[int] = None
    borrower_name: Optional[str] = None
    borrow_date: Optional[datetime] = None
    return_date: Optional[datetime] = None

# Response Schema
class BorrowRecordResponse(BorrowRecordBase):
    id: int
    book: Optional["BookResponse"] = None

    class Config:
        from_attributes = True  # Enables ORM to dict conversion for SQLAlchemy models

# Generic Message Response
class MessageResponse(BaseModel):
    message: str

# Note: model_rebuild() removed to avoid circular dependency issues
# Forward references with quotes should work automatically