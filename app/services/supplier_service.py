from typing import List, Optional
from app.repositories.supplier_repository import SupplierRepository
from app.models.supplier import Supplier

class SupplierService:
    def __init__(self, repo: SupplierRepository):
        self.repo = repo

    def create(self, data) -> Supplier:
        return self.repo.create(**data.dict())

    def update(self, supplier_id: int, data) -> Supplier:
        return self.repo.update(supplier_id, **data.dict())

    def delete(self, supplier_id: int) -> bool:
        return self.repo.delete(supplier_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.repo.list_all(skip, limit)
