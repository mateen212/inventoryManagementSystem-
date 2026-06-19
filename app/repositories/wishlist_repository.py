from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.wishlist import Wishlist

class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self, db: Session):
        super().__init__(Wishlist, db)
