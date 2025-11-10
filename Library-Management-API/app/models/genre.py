from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    #Relationsip with Books
    books = relationship("Book", back_populates="genre", cascade="all, delete-orphan") # 1:N relationship

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
