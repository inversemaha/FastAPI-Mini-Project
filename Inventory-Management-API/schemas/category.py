from pydantic import BaseModel
from typing import Optional

# --- Base Schema (common fields) ---
class CategoryBase(BaseModel):
    name: str

# --- Create Schema ---
class CategoryCreate(CategoryBase):
    pass

# --- Update Schema ---
class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

# --- Response Schema ---
class CategoryResponse(CategoryBase):
    id: int

    class config:
        orm = True  # Enables ORM to dict conversion for SQLAlchemy models


# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str