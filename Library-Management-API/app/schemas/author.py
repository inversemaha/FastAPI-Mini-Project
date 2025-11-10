from pydantic import BaseModel
from typing import Optional

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

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str