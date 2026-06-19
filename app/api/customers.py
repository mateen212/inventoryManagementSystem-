from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.core.dependencies import require_admin, require_authenticated
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserOut
from app.models.user import User
from app.core.roles import UserRole

router = APIRouter()

# ========== ADMIN ENDPOINTS ==========

@router.get("/", response_model=List[UserOut])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all customers (admin only)."""
    customers = db.query(User).filter(
        User.role.has(name=UserRole.CUSTOMER.value)
    ).offset(skip).limit(limit).all()
    return customers

@router.get("/search", response_model=List[UserOut])
def search_customers(
    q: str = Query(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Search customers by name or email (admin only)."""
    results = db.query(User).filter(
        User.role.has(name=UserRole.CUSTOMER.value),
        ((User.full_name.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")))
    ).all()
    return results

@router.get("/{customer_id}", response_model=UserOut)
def get_customer(
    customer_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get customer details (admin only)."""
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.get_by_id(customer_id)
    if not user or user.role.name != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=404, detail="Customer not found")
    return user

@router.put("/{customer_id}", response_model=UserOut)
def update_customer(
    customer_id: int,
    data: dict,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update customer information (admin only)."""
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.get_by_id(customer_id)
    if not user or user.role.name != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Allow updating specific fields
    allowed_fields = {"full_name", "email"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    if not update_data:
        return user
    
    return service.update_user(customer_id, update_data)

@router.post("/{customer_id}/disable")
def disable_customer(
    customer_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Disable a customer account (admin only)."""
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.get_by_id(customer_id)
    if not user or user.role.name != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    service.disable_user(customer_id)
    return {"message": "Customer account disabled"}

@router.post("/{customer_id}/enable")
def enable_customer(
    customer_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Enable a customer account (admin only)."""
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.get_by_id(customer_id)
    if not user or user.role.name != UserRole.CUSTOMER.value:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    service.enable_user(customer_id)
    return {"message": "Customer account enabled"}
