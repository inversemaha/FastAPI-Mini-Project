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

    model_config = {"from_attributes": True}  # Pydantic v2: enables ORM attribute access


# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str