from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from models.supplier import Supplier as SupplierModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/supplier", tags=["Suppliers"])

@router.get("/", response_model=list[SupplierResponse])
def get_suppliers(skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    db_suppliers = db.query(SupplierModel).offset(skip).limit(limit).all()
    if not db_suppliers:
        raise HTTPException(status_code=404, detail="Suppliers not found")
    return db_suppliers

@router.get("/{id}", response_model=SupplierResponse)
def get_suppliers_by_id(id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(SupplierModel).filter(SupplierModel.id == id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.post("/", response_model=SupplierResponse)
def add_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    # Fetch suppliers from response body
    try:
        db_supplier = SupplierModel(supplier.model_dump())
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Supplier already exist")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")

@router.put("/{id}", response_model=SupplierResponse)
def update_supplier(id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = db.query(SupplierModel).filter(SupplierModel.id == id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    #Update Supplier
    try:
        for key, value in supplier.model_dump().items():
            setattr(db_supplier, key, value)
        db.commit()
        db.refresh(db_supplier)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to update supplier")

@router.delete("/{id}")
def delete_supplier(id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(SupplierModel).filter(SupplierModel.id == id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    try:
        db.delete(db_supplier)
        db.commit()
        return {"message": "Supplier deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to delete supplier")