from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

# Initialize category class
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(198), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationship with Products
    products = relationship("Product", back_populates="category")