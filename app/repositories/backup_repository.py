from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.backup import Backup

class BackupRepository(BaseRepository[Backup]):
    def __init__(self, db: Session):
        super().__init__(Backup, db)
