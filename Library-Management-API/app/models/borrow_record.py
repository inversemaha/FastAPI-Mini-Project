from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String, nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    #Relationship with Book
    books = relationship("Book", back_populates="borrow_records") # N:1 relationship

    def __repr__(self):
        return f"<BorrowRecord(id={self.id}, borrower='{self.borrower_name}', book_id={self.book_id})>"
