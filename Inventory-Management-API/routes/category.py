from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from models.category import Category as CategoryModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/category", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_all_category(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).offset(skip).limit(limit).all()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categories not found")
    return db_category

@router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    db_category= db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categories not found")
    return db_category

@router.post("/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Fetch category data from request body
    try:
        db_category = CategoryModel(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Category already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")

@router.put("/{id}", response_model=CategoryUpdate)
def update_category(id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    # Fetch Catefory From DB
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    #Update category
    try:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update category")

@router.delete("/{id}")
def delete_category(id:int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category ot found")
    try:
        db.delete(db_category)
        db.commit()
        return {"message": "Category deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete category")