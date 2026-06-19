from sqlalchemy.orm import Session
from app.models.category import Category
from app.repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)
