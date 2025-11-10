from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from config.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    #Relationship with Book
    books = relationship("Book", back_populates="author")