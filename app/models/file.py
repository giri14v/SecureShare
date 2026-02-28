from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)

    token = Column(String, unique=True, index=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    max_downloads = Column(Integer, nullable=True)
    download_count = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="files")