from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UploadResponse(BaseModel):
    download_url : str
    token : str
    expires_at : datetime
    max_downloads : Optional[int]