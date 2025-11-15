from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

# Initialize Supplier Class
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    contact_info = Column(Text, nullable=False)
    
    # Relationship with StockEntry
    stock_entries = relationship("StockEntry", back_populates="supplier")