from pydantic import BaseModel
from datetime import datetime

class BackupBase(BaseModel):
    filename: str
    path: str
    size: int

class BackupCreate(BackupBase):
    pass

class BackupOut(BackupBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
