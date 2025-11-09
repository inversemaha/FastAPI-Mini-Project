from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from models.product import Product as ProductModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/product", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_all_products(skip: int =0, limit: int =10, db: Session = Depends(get_db)):
    db_products = db.query(ProductModel).offset(skip).limit(limit).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_products

@router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_products = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_products

@router.post("/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    # fetch product data from request body
    try:
        db_products = ProductModel(**product.model_dump())
        db.add(db_products)
        db.commit()
        db.refresh(db_products)
        return db_products
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Product already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")
    
@router.put('/{id}', response_model=ProductResponse)
def update_product(id: int, product:ProductUpdate, db: Session = Depends(get_db)):
    db_products = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    #Update Product
    try:
        for key, value in product.model_dump().items():
            setattr(db_products, key, value)
        db.commit()
        db.refresh(db_products)
        return db_products
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to update product")

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted succefully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to delete Product")