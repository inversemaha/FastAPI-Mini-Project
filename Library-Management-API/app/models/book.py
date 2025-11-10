from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    publication_year = Column(Integer, nullable=False)

    #Relationship with Author & Genre
    author = relationship("Author", back_populates="books")  # N:1 relationship
    genre = relationship("Genre", back_populates="books")  # N:1 relationship
    borrow_records = relationship("BorrowRecord", back_populates="book", cascade="all, delete-orphan")  # 1:N relationship

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"