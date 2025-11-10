from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.book import BookResponse

# Base Schema
class AuthorBase(BaseModel):
    name: str
    country: Optional[str] = None

#Create Schema
class AuthorCreate(AuthorBase):
    pass

#Update Schema
class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None

#--- Response Schema -----
class AuthorResponse(AuthorBase):
    id: int
    books: List["BookResponse"] = [] # 1:N relationship

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

AuthorResponse.model_rebuild()

# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str