from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.core.dependencies import require_admin
from app.models.user import User

router = APIRouter()

# ========== CUSTOMER ENDPOINTS (Read-only) ==========

@router.get("/", response_model=List[CategoryOut])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all categories (customer and admin can view)."""
    repo = CategoryRepository(db)
    service = CategoryService(repo)
    return service.list_all(skip, limit)

# ========== ADMIN ENDPOINTS (Write operations) ==========

@router.post("/", response_model=CategoryOut)
def create_category(
    data: CategoryCreate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new category (admin only)."""
    repo = CategoryRepository(db)
    service = CategoryService(repo)
    return service.create(data)

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int, 
    data: CategoryUpdate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update category details (admin only)."""
    repo = CategoryRepository(db)
    service = CategoryService(repo)
    try:
        return service.update(category_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a category (admin only)."""
    repo = CategoryRepository(db)
    service = CategoryService(repo)
    if not service.delete(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}
