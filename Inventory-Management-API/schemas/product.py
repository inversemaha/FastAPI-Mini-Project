from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING 

if TYPE_CHECKING:
    from schemas.category import CategoryResponse

# --- Base Schema (common fields) ---
class ProductBase(BaseModel):
    name: str
    sku: str
    description: Optional[str] = Field(None, max_length=1000)
    price: float
    quantity: int
    category_id: int

# --- Create Schema ---
class ProductCreate(ProductBase):
    pass

# --- Update Schema (all fields optional for partial update) ---
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None

# --- Response Schema ---
class ProductResponse(ProductBase):
    id: int
    category: Optional["CategoryResponse"] = None  # forward reference

    model_config = {"from_attributes": True}  # Pydantic v2: enables ORM attribute access

# --- Generic message response ---
class MessageResponse(BaseModel):
    message: str