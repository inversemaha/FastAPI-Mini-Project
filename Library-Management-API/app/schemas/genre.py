from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.book import BookResponse

#Base Schema
class GenreBase(BaseModel):
    name: str

#Create Schema
class GenreCreate(GenreBase):
    pass

#Update Schema
class GenreUpdate(BaseModel):
    name: Optional[str] = None

#Response Schema
class GenreResponse(GenreBase):
    id: int
    books: List["BookResponse"] = [] # 1:N relationship

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

GenreResponse.model_rebuild()

# Generic Message Response
class MessageResponse(BaseModel):
    message: str