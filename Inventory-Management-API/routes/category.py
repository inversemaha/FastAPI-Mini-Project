from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from models.category import Category as CategoryModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_all_category(db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).all()
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
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{id}", response_model=CategoryUpdate)
def update_category(id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    # Fetch Catefory From DB
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    #Update category
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{id}")
def delete_category(id:int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category ot found")
    db.delete(db_category)
    db.commit()
    db.refresh()
    return {"message": "Category deleted successfully"}