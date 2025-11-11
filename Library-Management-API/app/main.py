from fastapi import FastAPI
from app.routes import author, genre, book, borrow_record

# Rebuild models to resolve forward references
from app.schemas.author import AuthorResponse
from app.schemas.genre import GenreResponse
from app.schemas.book import BookResponse
from app.schemas.borrow_record import BorrowRecordResponse
AuthorResponse.model_rebuild()
GenreResponse.model_rebuild()
BookResponse.model_rebuild()
BorrowRecordResponse.model_rebuild()

# Initilize FastAPI
app = FastAPI()

@app.get("/")
def greet():
    return " This Text is for Test"

#Register Route under main.py
app.include_router(author.router)
app.include_router(genre.router)
app.include_router(book.router)
app.include_router(borrow_record.router)
