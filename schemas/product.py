from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING 

if TYPE_CHECKING:
    from schemas.category import CategoryResponse
    
# --- Base Schema (common fields) ---
class ProductBase(BaseModel):
    name: str
    sku: str
    description: Optional[str] = Field(None, max_length=1000)
    price: float  # Standard/retail selling price
    category_id: int

# --- Create Schema ---
class ProductCreate(ProductBase):
    pass

# --- Update Schema (all fields optional for partial update) ---
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = None  # Standard/retail selling price
    category_id: Optional[int] = None

# --- Response Schema ---
class ProductResponse(ProductBase):
    id: int
    category: Optional["CategoryResponse"] = None  # forward reference

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str