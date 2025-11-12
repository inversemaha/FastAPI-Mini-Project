from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    publication_year = Column(Integer, nullable=False)
    total_copies = Column(Integer, nullable=False, default=1)  # Total number of copies

    # Relationships
    author = relationship("Author")  # N:1 relationship - Book → Author
    genre = relationship("Genre")   # N:1 relationship - Book → Genre

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"