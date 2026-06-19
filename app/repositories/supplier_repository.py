from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.repositories.base_repository import BaseRepository

class SupplierRepository(BaseRepository[Supplier]):
    def __init__(self, db: Session):
        super().__init__(Supplier, db)
