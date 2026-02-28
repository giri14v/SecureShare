from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.file_service import FileService

router = APIRouter()

@router.get("/download/{token}")
def download_file(token:str, db: Session = Depends(get_db)):
    # Fetch File record
    db_file = FileService.get_file_by_token(token,db)

    return FileResponse(
        path = db_file.stored_path,
        filename= db_file.filename,
        media_type="application/octet-stream"
    )