from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from schemas.stockEntry import StockEntryCreate, StockEntryUpdate, StockEntryResponse
from models.stockEntry import StockEntry as StockEntryModel
from models.product import Product as ProductModel
from models.supplier import Supplier as SupplierModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

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
    # Validate that product exists
    product = db.query(ProductModel).filter(ProductModel.id == stock_entry.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate that supplier exists
    supplier = db.query(SupplierModel).filter(SupplierModel.id == stock_entry.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Backend validation and business rules
    if stock_entry.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    if stock_entry.unit_price <= 0:
        raise HTTPException(status_code=400, detail="Unit price must be positive")
    
    # Create stock entry - backend handles all calculations
    try:
        db_stock_entry = StockEntryModel(**stock_entry.model_dump())
        db.add(db_stock_entry)
        db.commit()
        db.refresh(db_stock_entry)        
        return db_stock_entry
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Stock entry validation failed")
    except Exception as e:
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
    
@router.get("/by-product/{product_id}")
def get_stock_by_product(product_id: int, db: Session = Depends(get_db)):
    """Get all stock entries for a specific product"""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    stock_entries = db.query(StockEntryModel).filter(StockEntryModel.product_id == product_id).all()
    
    # Calculate total stock for this product
    total_stock = db.query(func.sum(StockEntryModel.quantity)).filter(
        StockEntryModel.product_id == product_id
    ).scalar() or 0
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_stock": total_stock,
        "stock_entries": stock_entries
    }

@router.get("/by-supplier/{supplier_id}")
def get_stock_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """Get all stock entries for a specific supplier"""
    supplier = db.query(SupplierModel).filter(SupplierModel.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    stock_entries = db.query(StockEntryModel).filter(StockEntryModel.supplier_id == supplier_id).all()
    
    return {
        "supplier_id": supplier_id,
        "supplier_name": supplier.name,
        "stock_entries": stock_entries
    }

@router.get("/low-stock")
def get_low_stock_products(threshold: int = 10, db: Session = Depends(get_db)):
    """Get products with total stock below threshold"""
    # Group by product and calculate total stock
    results = db.query(
        ProductModel.id,
        ProductModel.name,
        ProductModel.price,
        ProductModel.sku,
        func.sum(StockEntryModel.quantity).label('total_stock')
    ).join(
        StockEntryModel, ProductModel.id == StockEntryModel.product_id
    ).group_by(
        ProductModel.id, ProductModel.name, ProductModel.price, ProductModel.sku
    ).having(
        func.sum(StockEntryModel.quantity) <= threshold
    ).all()
    
    return [
        {
            "product_id": result.id,
            "product_name": result.name,
            "sku": result.sku,
            "price": result.price,
            "current_stock": int(result.total_stock),
            "threshold": threshold,
            "status": "LOW_STOCK"
        }
        for result in results
    ]



@router.delete("/{id}")
def delete_stock_entry(id: int, db: Session = Depends(get_db)):
    db_stock_entry = db.query(StockEntryModel).filter(StockEntryModel.id == id).first()
    if not db_stock_entry:
        raise HTTPException(status_code=404, detail="Stock entry not found")
        
    try:
        db.delete(db_stock_entry)
        db.commit()
        return {"message": "Stock entry deleted successfully"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete stock entry")