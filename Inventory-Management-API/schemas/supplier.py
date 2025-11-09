from pydantic import BaseModel, Field
from typing import Optional

# --- Base Schema (common fields) ---
class SupplierBase(BaseModel):
    name: str
    phone: str = Field(..., pattern=r"^\+?\d{10,15}$")  # ✅ Optional validation
    contact_info: str

# Create Schema
class SupplierCreate(SupplierBase):
    pass

# Update Schema
class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")  # ✅ Optional validation
    contact_info: Optional[str] = None

# --- Response Schema ---
class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True # Enables ORM to dict conversion for SQLAlchemy models

# General Message response
class MessageResponse(BaseModel):
    message: str