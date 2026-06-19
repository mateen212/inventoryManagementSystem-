from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_authenticated
from app.models.user import User

router = APIRouter()

# ========== CUSTOMER ENDPOINTS (Own wishlist only) ==========

@router.get("/")
def get_wishlist(
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Get current user's wishlist."""
    # TODO: Implement wishlist retrieval
    return {"user_id": current_user.id, "items": []}

@router.post("/add")
def add_to_wishlist(
    product_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Add product to wishlist."""
    # TODO: Implement add to wishlist
    return {"message": "Product added to wishlist", "product_id": product_id}

@router.delete("/{item_id}")
def remove_from_wishlist(
    item_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Remove item from wishlist."""
    # TODO: Implement remove from wishlist
    return {"message": "Item removed from wishlist"}

@router.post("/{item_id}/move-to-cart")
def move_to_cart(
    item_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Move wishlist item to cart."""
    # TODO: Implement move to cart
    return {"message": "Item moved to cart"}
