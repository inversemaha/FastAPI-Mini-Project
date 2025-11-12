from pydantic import BaseModel
from datetime import datetime

#Base Schema
class BorrowRecordBase(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: datetime | None = None

#Create Schema
class BorrowRecordCreate(BorrowRecordBase):
    pass

#Update Schema
class BorrowRecordUpdate(BaseModel):
    book_id: int | None = None
    borrower_name: str | None = None
    borrow_date: datetime | None = None
    return_date: datetime | None = None

# Response Schema
class BorrowRecordResponse(BorrowRecordBase):
    id: int
    
    class Config:
        from_attributes = True  # Enables ORM to dict conversion for SQLAlchemy models

# Generic Message Response
class MessageResponse(BaseModel):
    message: str

# Note: model_rebuild() removed to avoid circular dependency issues
# Forward references with quotes should work automatically