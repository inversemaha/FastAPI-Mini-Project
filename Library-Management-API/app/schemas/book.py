from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

#Tyoe Cheking for Circular Relationship issue
if TYPE_CHECKING:
    from schemas.author import AuthorResponse
    from schemas.genre import GenreResponse

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
class BookResponse(BaseModel):
    id: int
    author: Optional["AuthorResponse"] = None  # Fowarad Reffrence
    genre: Optional["GenreResponse"] = None  # Fowared Reffrence

    class Config:
        from_attributs = True  # Enables ORM to dict conversion for SQLAlchemy models

# Generic Message Response
class MessageResponse(BaseModel):
    message: str