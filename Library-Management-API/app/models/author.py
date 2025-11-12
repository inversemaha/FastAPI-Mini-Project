from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship
from app.config.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
