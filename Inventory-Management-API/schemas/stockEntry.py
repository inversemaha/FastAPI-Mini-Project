from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.product import ProductResponse
    from schemas.supplier import SupplierResponse

# -- Base Schema (Common fields) --
class StockEntryBase(BaseModel):
    product_id: int
    supplier_id: int
    quantity: int
    unit_price: Optional[float] = None
    due_date: Optional[datetime] = None

# Create Schema
class StockEntryCreate(StockEntryBase):
    pass

# -- Update Schema (all optional for partial updates) --
class StockEntryUpdate(BaseModel):
    product_id: Optional[int] = None
    supplier_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    due_date: Optional[datetime] = None

# Response Schema
class StockEntryResponse(BaseModel):
    id: int
    # product_id: int
    # supplier_id: int
    # quantity: int
    # unit_price: Optional[float] = None
    # due_date: Optional[datetime] = None
    product: Optional["ProductResponse"] = None
    supplier: Optional["SupplierResponse"] = None

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

# -- Generic Message response
class MessageResponse(BaseModel):
    message: str
