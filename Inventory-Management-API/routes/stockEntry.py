from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.stockEntry import StockEntryCreate, StockEntryUpdate, StockEntryResponse
from models.stockEntry import StockEntry as StockEntryModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/stock_entries", tags=["Stock Entry"])

@router.get("/", response_model=list[StockEntryResponse])
def get_all_stock_entries(skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    stock_entries = db.query(StockEntryModel).offset(skip).limit(limit).all()
    if not stock_entries:
        raise HTTPException(status_code=404, detail="Stock entries not found")
    return stock_entries

@router.get("/{id}", response_model=StockEntryResponse)
def get_single_stock_entries(id: int, db: Session = Depends(get_db)):
    single_stock_entry = db.query(StockEntryModel).filter(StockEntryModel.id == id).first()
    if not single_stock_entry:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    return single_stock_entry

@router.post("/", response_model=StockEntryResponse)
def add_stock_entries(stock_entry: StockEntryCreate, db: Session = Depends(get_db)):
    #Fetch data form resquest body
    try:
        db_stock_entry  = StockEntryModel(**stock_entry.model_dump())
        db.add(db_stock_entry )
        db.commit()
        db.refresh(db_stock_entry )
        return db_stock_entry 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Stock entry already exist")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Server error")

@router.put("/{id}", response_model=StockEntryResponse)
def update_stock_entry(id: int, stock_entry: StockEntryUpdate, db: Session = Depends(get_db)):
    db_stock_entry = db.query(StockEntryModel).filter(StockEntryModel.id == id).first()
    if not db_stock_entry:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    
    try:
        for key, value in stock_entry.model_dump().items():
            setattr(db_stock_entry, key, value)
        db.commit()
        db.refresh(db_stock_entry)
        return db_stock_entry
    except Exception:
        db.rollback()
        raise HTTPException(status_code=404, detail="Stock entry not found")
    
@router.delete("/{id}")
def delete_stock_entry(id: int, db: Session = Depends(get_db)):
    db_stock_entry = db.query(StockEntryModel).filter(StockEntryModel.id == id).first()
    if not db_stock_entry:
        raise HTTPException(status_code=404, detail="Stock entry not found")
        
    try:
        db.delete(db_stock_entry)
        db.commit()
        return {"message": "Product deleted succefully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failled to delete Product")