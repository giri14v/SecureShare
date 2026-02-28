import os
from datetime import datetime, timedelta
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.file_schema import UploadResponse
from app.services.file_service import FileService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload", response_model= UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
     expiry_minutes: int = Form(None),
     max_downloads: int = Form(None),
     db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)
):
    db_file = await FileService.create_file(
        file=file,
        expiry_minutes=expiry_minutes,
        max_downloads= max_downloads,
        user_id= current_user.id,
        db = db
    )

    return UploadResponse(
        download_url=  f"/download/{db_file.token}",
        token = db_file.token,
        expires_at= db_file.expires_at,
        max_downloads= db_file.max_downloads
    )