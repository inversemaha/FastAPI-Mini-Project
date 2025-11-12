from pydantic import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING

# Type checking for relationships
if TYPE_CHECKING:
    from .author import AuthorResponse
    from .genre import GenreResponse

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
    title: str | None = None
    author_id: int | None = None
    genre_id: int | None = None
    publication_year: int | None = None

#Response Schema
class BookResponse(BookBase):
    id: int
    author: "AuthorResponse | None" = None  # N:1 Forward Reference
    genre: "GenreResponse | None" = None  # N:1 Forward Reference

    class Config:
        from_attributes = True  # Enables ORM to dict conversion for SQLAlchemy models

# Generic Message Response
class MessageResponse(BaseModel):
    message: str

# Note: Using schema registry pattern for model rebuilding