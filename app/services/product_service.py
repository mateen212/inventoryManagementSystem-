from typing import Optional, List
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create(self, data: ProductCreate) -> Product:
        return self.repo.create(data)

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        return self.repo.update(product_id, data)

    def delete(self, product_id: int) -> bool:
        return self.repo.delete(product_id)

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.repo.get_by_id(product_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repo.list_all(skip, limit)

    def search(self, query: str) -> List[Product]:
        return self.repo.search(query)
