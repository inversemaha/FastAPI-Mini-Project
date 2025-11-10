from fastapi import FastAPI
from routes import author, book, borrow_record, genre

# Initilize FastAPI
app = FastAPI()

@app.get("/")
def greet():
    return " This Text is for Test"

#Register Route under main.py
