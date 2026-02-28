import os
from datetime import datetime, timedelta
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.exceptions import (
    FileNotFoundError,
    LinkExpiredError,
    DownloadLimitReachedError,
    InvalidExpiryError,
    InvalidDownloadLimitError
)
from app.core.logger import logger

from app.models.file import File as FileModel
from app.services.token_service import generate_secure_token
from app.core.config import settings

class FileService:
    @staticmethod
    async def create_file(
        file: UploadFile,
        expiry_minutes: int,
        max_downloads: int | None,
        user_id: int,
        db: Session
    ):
        # Default Expiry
        if expiry_minutes is None:
            expiry_minutes = settings.DEFAULT_EXPIRY_MINUTES

        # Expiry Validation
        if expiry_minutes < settings.MIN_EXPIRY_MINUTES or expiry_minutes > settings.MAX_EXPIRY_MINUTES:
            raise InvalidExpiryError()
        
        # Download limit validation
        if max_downloads is not None and max_downloads <= 0:
            raise InvalidDownloadLimitError()
        
        token = generate_secure_token()
        expires_at = datetime.utcnow() + timedelta(minutes= expiry_minutes)

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        stored_filename = f"{token}_{file.filename}"
        stored_path = os.path.join(settings.UPLOAD_DIR, stored_filename)

        with open(stored_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        db_file = FileModel(
            filename = file.filename,
            stored_path = stored_path,
            token = token,
            expires_at = expires_at,
            max_downloads = max_downloads,
            download_count = 0,
            user_id = user_id
        )
        db.add(db_file)
        db.commit()
        logger.info(
            "file_uploaded",
            extra={
                "extra_data": {
                    "event": "file_uploaded",
                    "user_id": user_id,
                    "token": token,
                    "expires_at": str(expires_at),
                    "max_downloads": max_downloads
                }
            }
        )
        db.refresh(db_file)

        return db_file
    
    @staticmethod
    def get_file_by_token(token: str, db: Session):
        db_file = db.query(FileModel).filter(FileModel.token == token).first()

        if not db_file:
            raise FileNotFoundError()
        
        if datetime.utcnow() > db_file.expires_at:
            logger.warning(
                "link_expired_attempt",
                extra={
                    "extra_data": {
                        "event": "link_expired",
                        "token": token,
                        "user_id": db_file.user_id
                    }
                }
            )
            raise LinkExpiredError()
        
        if db_file.max_downloads is not None:
            if db_file.download_count >= db_file.max_downloads:
                logger.warning(
                    "download_limit_hit",
                    extra={
                        "extra_data": {
                            "event": "download_limit_hit",
                            "token": token,
                            "user_id": db_file.user_id
                        }
                    }
                )
                raise DownloadLimitReachedError()
            
        if not os.path.exists(db_file.stored_path):
            raise FileNotFoundError()
        
        db_file.download_count += 1
        logger.info(
            "file_downloaded",
            extra={
                "extra_data": {
                    "event": "file_downloaded",
                    "token": token,
                    "user_id": db_file.user_id,
                    "download_count": db_file.download_count
                }
            }
        )
        db.commit()

        return db_file