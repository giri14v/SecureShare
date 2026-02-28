import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.file import File as FileModel
from app.core.logger import logger

def cleanup_expired_files(db: Session):
    expired_files = (
        db.query(FileModel)
        .filter(FileModel.expires_at < datetime.utcnow())
        .all()
    )

    for file in expired_files:
        # delete file from disk
        if os.path.exists(file.stored_path):
            os.remove(file.stored_path)

        logger.info(
            "file_cleanup",
            extra={
                "extra_data": {
                    "event": "file_cleanup",
                    "file_id": file.id,
                    "token": file.token,
                    "user_id": file.user_id
                }
            }
        )

        # delete DB row
        db.delete(file)

    db.commit()