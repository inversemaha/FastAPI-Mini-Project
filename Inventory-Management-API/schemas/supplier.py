from pydantic import BaseModel
from typing import Optional

# --- Base Schema (common fields) ---
class SupplierBase(BaseModel):
    name = str
    contact_info = str

# Create Schema
class SupplierCreate(SupplierBase):
    pass

# Update Schema
class SupplierUpdate(BaseModel):
    name = Optional(str) = None
    contact_info = Optional(str) = None

# --- Response Schema ---
class SupplierResponse(SupplierBase):
    id = int

    class Config:
        orm_mode = True # Enables ORM to dict conversion for SQLAlchemy models

# General Message response
class MessageResponse(BaseModel):
    message: str