from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.order import Order

class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: Session):
        super().__init__(Order, db)
