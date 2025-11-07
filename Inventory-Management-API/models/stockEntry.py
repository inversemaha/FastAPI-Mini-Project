from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

#Initilized StokEntry class
class StockEntry(Base):
    __tablename__ = "stock_entries"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products_id"),nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers_id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    unit_price = Column(Float, nullable=True)
    due_date = Column(DateTime, default=datetime.utcnow)

    #Relationship with Category
    product = relationship("Product", back_populates="stock_entries")
    supplier = relationship("Supplier", back_populates="stock_entries")