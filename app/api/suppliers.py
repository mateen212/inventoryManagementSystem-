from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.supplier_service import SupplierService
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierOut
from app.core.dependencies import require_admin
from app.models.user import User

router = APIRouter()

# ========== ADMIN ENDPOINTS ==========

@router.get("/", response_model=List[SupplierOut])
def list_suppliers(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all suppliers (admin only)."""
    repo = SupplierRepository(db)
    service = SupplierService(repo)
    return service.list_all(skip, limit)

@router.post("/", response_model=SupplierOut)
def create_supplier(
    data: SupplierCreate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new supplier (admin only)."""
    repo = SupplierRepository(db)
    service = SupplierService(repo)
    return service.create(data)

@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(
    supplier_id: int, 
    data: SupplierUpdate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update supplier details (admin only)."""
    repo = SupplierRepository(db)
    service = SupplierService(repo)
    try:
        return service.update(supplier_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Supplier not found")

@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: int, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a supplier (admin only)."""
    repo = SupplierRepository(db)
    service = SupplierService(repo)
    if not service.delete(supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"detail": "Supplier deleted successfully"}
