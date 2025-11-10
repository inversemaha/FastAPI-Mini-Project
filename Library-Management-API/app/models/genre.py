from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    #Relationsip with Books
    books = relationship("Book", back_populates="genre")