from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

#Initilized Supplier Class
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    
    #Relationship with StockEntry
    stock_entries = relationship("StockEntry", back_populates="supplier")