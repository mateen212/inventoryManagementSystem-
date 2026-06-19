from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.invoice import Invoice

class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db: Session):
        super().__init__(Invoice, db)
