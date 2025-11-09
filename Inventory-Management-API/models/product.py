from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


#Initilize Product class
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    sku = Column(String, unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    #Relationship with Category
    category = relationship("Category", back_populates="products")
    
    #Relationship with StockEntry
    stock_entries = relationship("StockEntry", back_populates="product")