from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.dependencies import require_authenticated
from app.models.user import User
from app.models.wishlist import Wishlist
from app.models.product import Product

router = APIRouter()


@router.get("/")
def get_wishlist(
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    items = []
    q = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    for w in q:
        items.append({
            "id": w.id,
            "product_id": w.product_id,
            "name": getattr(w.product, 'name', None),
            "sku": getattr(w.product, 'sku', None),
            "price": getattr(w.product, 'selling_price', None)
        })
    return {"user_id": current_user.id, "items": items}


@router.post("/add")
def add_wishlist(product_id: int, current_user: User = Depends(require_authenticated), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = db.query(Wishlist).filter(Wishlist.user_id == current_user.id, Wishlist.product_id == product_id).first()
    if existing:
        return {"message": "Already in wishlist"}
    w = Wishlist(user_id=current_user.id, product_id=product_id)
    db.add(w)
    db.commit()
    db.refresh(w)
    return {"message": "Added", "id": w.id}


@router.delete("/{wishlist_id}")
def remove_wishlist(wishlist_id: int, current_user: User = Depends(require_authenticated), db: Session = Depends(get_db)):
    w = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not w:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    if w.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(w)
    db.commit()
    return {"message": "Removed"}
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
