from fastapi import FastAPI
from config.database import engine, Base
from routes import category

# Import models to ensure they're registered with base
from models.category import Category

# Create all tables in correct order (Base knows the dependencies)
Base.metadata.create_all(bind=engine)

#initilize FastAPI app
app = FastAPI()

#Test a text

@app.get("/")
def greet():
    return "This is test text"

app.include_router(category.router)