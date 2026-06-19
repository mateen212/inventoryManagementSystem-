from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.settings import Settings

class SettingsRepository(BaseRepository[Settings]):
    def __init__(self, db: Session):
        super().__init__(Settings, db)
