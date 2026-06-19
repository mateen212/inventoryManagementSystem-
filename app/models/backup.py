from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Backup(Base):
    __tablename__ = "backups"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    path = Column(String(500))
    size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
