from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

#Tyoe Cheking for Circular Relationship issue
if TYPE_CHECKING:
    from schemas.author import AuthorResponse
    from schemas.genre import GenreResponse
    from schemas.borrow_record import BorrowRecordResponse

#Base Schema
class BookBase(BaseModel):
    title: str
    author_id: int
    genre_id: int
    publication_year: int

#Create Schema
class BookCreate(BookBase):
    pass

#Update Schema
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    genre_id: Optional[int] = None
    publication_year: Optional[int] = None

#Response Schema
class BookResponse(BookBase):
    id: int
    author: Optional["AuthorResponse"] = None  # N:1 Forward Reference
    genre: Optional["GenreResponse"] = None  # N:1 Forward Reference
    borrow_records: List["BorrowRecordResponse"] = []  # 1:N relationship

    class Config:
        from_attributes = True  # Enables ORM to dict conversion for SQLAlchemy models

BookResponse.model_rebuild()

# Generic Message Response
class MessageResponse(BaseModel):
    message: str