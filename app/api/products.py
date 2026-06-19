from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.core.dependencies import require_admin, require_authenticated
from app.models.user import User

router = APIRouter()

# ========== CUSTOMER ENDPOINTS (Read-only) ==========

@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """List all products (customer and admin can view)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.list_all(skip, limit)

@router.get("/search", response_model=List[ProductOut])
def search_products(
    q: str = Query(...), 
    db: Session = Depends(get_db)
):
    """Search products by query (customer and admin can search)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.search(q)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    """Get product details (customer and admin can view)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ========== ADMIN ENDPOINTS (Write operations) ==========

@router.post("/", response_model=ProductOut)
def create_product(
    data: ProductCreate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new product (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    return service.create(data)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int, 
    data: ProductUpdate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update product details (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    try:
        return service.update(product_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a product (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    if not service.delete(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

@router.post("/{product_id}/upload-images")
async def upload_product_images(
    product_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Upload multiple images for a product (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # TODO: Implement image upload logic
    return {"detail": f"Uploaded {len(files)} images", "product_id": product_id}

@router.post("/{product_id}/generate-barcode")
def generate_product_barcode(
    product_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Generate barcode for a product (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # TODO: Implement barcode generation logic
    return {"detail": "Barcode generated", "product_id": product_id, "barcode": "123456789"}

@router.post("/{product_id}/generate-qrcode")
def generate_product_qrcode(
    product_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Generate QR code for a product (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # TODO: Implement QR code generation logic
    return {"detail": "QR code generated", "product_id": product_id, "qrcode_url": "/static/qrcodes/product_123.png"}

@router.post("/{product_id}/manage-stock")
def manage_product_stock(
    product_id: int,
    quantity: int = Query(...),
    action: str = Query(..., regex="^(add|subtract|set)$"),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Manage product stock (admin only)."""
    repo = ProductRepository(db)
    service = ProductService(repo)
    
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # TODO: Implement stock management logic
    return {"detail": f"Stock {action} completed", "product_id": product_id, "new_quantity": 0}
