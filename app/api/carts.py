from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.dependencies import require_customer, require_authenticated
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus
from datetime import datetime

router = APIRouter()


def _get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/")
def get_cart(
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Get current user's cart."""
    cart = _get_or_create_cart(db, current_user.id)
    items = []
    for it in cart.items:
        items.append({
            "id": it.id,
            "product_id": it.product_id,
            "name": getattr(it.product, 'name', None),
            "sku": getattr(it.product, 'sku', None),
            "quantity": it.quantity,
            "price": it.price,
            "total": (it.price or 0.0) * (it.quantity or 0)
        })
    return {"user_id": current_user.id, "items": items}


@router.post("/add")
def add_to_cart(
    product_id: int,
    quantity: int = 1,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Add product to cart."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be >= 1")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity <= 0:
        raise HTTPException(status_code=400, detail="Product out of stock")
    if quantity > product.quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.quantity} items available")

    cart = _get_or_create_cart(db, current_user.id)
    # find existing item
    existing = None
    for it in cart.items:
        if it.product_id == product.id:
            existing = it
            break

    if existing:
        new_qty = existing.quantity + quantity
        if new_qty > product.quantity:
            raise HTTPException(status_code=400, detail=f"Only {product.quantity} items available")
        existing.quantity = new_qty
        db.add(existing)
    else:
        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity, price=product.selling_price)
        db.add(item)

    db.commit()
    return get_cart(current_user=current_user, db=db)


@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Remove item from cart."""
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart = db.query(Cart).filter(Cart.id == item.cart_id).first()
    if not cart or cart.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(item)
    db.commit()
    return get_cart(current_user=current_user, db=db)


@router.put("/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Update item quantity in cart."""
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity must be >= 0")
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart = db.query(Cart).filter(Cart.id == item.cart_id).first()
    if not cart or cart.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if quantity == 0:
        db.delete(item)
        db.commit()
        return get_cart(current_user=current_user, db=db)
    if quantity > product.quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.quantity} items available")
    item.quantity = quantity
    db.add(item)
    db.commit()
    return get_cart(current_user=current_user, db=db)


@router.post("/checkout")
def checkout(
    current_user: User = Depends(require_authenticated),
    db: Session = Depends(get_db)
):
    """Checkout cart and create order."""
    cart = _get_or_create_cart(db, current_user.id)
    if not cart.items or len(cart.items) == 0:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # create order
    order = Order(customer_id=current_user.id, order_number=f"ORD{int(datetime.utcnow().timestamp())}{current_user.id}", status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    db.refresh(order)

    total = 0.0
    for it in list(cart.items):
        product = db.query(Product).filter(Product.id == it.product_id).with_for_update().first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail="Product not found")
        if it.quantity > product.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Only {product.quantity} items available for {product.name}")
        oi = OrderItem(order_id=order.id, product_id=product.id, quantity=it.quantity, price=it.price, total=(it.price or 0.0) * it.quantity)
        db.add(oi)
        product.quantity = product.quantity - it.quantity
        total += oi.total
        # remove cart item
        db.delete(it)

    order.total_amount = total
    db.add(order)
    db.commit()
    return {"message": "Order created", "order_id": order.id}
