from typing import List, Optional
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category

class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def create(self, data: CategoryCreate) -> Category:
        return self.repo.create(**data.dict())

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        return self.repo.update(category_id, **data.dict())

    def delete(self, category_id: int) -> bool:
        return self.repo.delete(category_id)

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.repo.get_by_id(category_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.repo.list_all(skip, limit)
