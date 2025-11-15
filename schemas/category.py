from pydantic import BaseModel
from typing import Optional

# --- Base Schema (common fields) ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

# --- Create Schema ---
class CategoryCreate(CategoryBase):
    pass

# --- Update Schema ---
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# --- Response Schema ---
class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models


# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str