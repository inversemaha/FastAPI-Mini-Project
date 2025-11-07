from sqlalchemy import Column, Integer, String, Text
from config.database import Base

#Initilized Supplier Class
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(Text, nullable=False)