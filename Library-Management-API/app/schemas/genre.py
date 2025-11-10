from pydantic import BaseModel
from typing import Optional

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

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

# Generic Message Response
class MessageResponse(BaseModel):
    message: str