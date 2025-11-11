from fastapi import FastAPI
from app.routes import author

# Initilize FastAPI
app = FastAPI()

@app.get("/")
def greet():
    return " This Text is for Test"

#Register Route under main.py
app.include_router(author.router)
