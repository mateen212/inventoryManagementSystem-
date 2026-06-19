from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(Product, db)

    def search(self, query: str) -> List[Product]:
        return self.db.query(Product).filter(
            Product.name.ilike(f"%{query}%") |
            Product.sku.ilike(f"%{query}%") |
            Product.barcode.ilike(f"%{query}%")
        ).all()
