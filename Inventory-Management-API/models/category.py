from sqlalchemy import Column, Integer, String
from config.database import Base

#Initilize category class
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(198), unique=True, index=True, nullable=False)