from fastapi import FastAPI
from config.database import engine, Base
from routes import category, product

# Import models to ensure they're registered with base
from models.category import Category
from models.product import Product

# Create all tables in correct order (Base knows the dependencies)
Base.metadata.create_all(bind=engine)

# Rebuild models to resolve forward references
from schemas.category import CategoryResponse
from schemas.product import ProductResponse
CategoryResponse.model_rebuild()
ProductResponse.model_rebuild()

#initilize FastAPI app
app = FastAPI()

#Test a text

@app.get("/")
def greet():
    return "This is test text"

app.include_router(category.router)
app.include_router(product.router)