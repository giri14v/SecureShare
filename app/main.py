from fastapi import FastAPI
from app.db.init_db import init_db
from app.routers import upload, download, auth
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    FileNotFoundError,
    LinkExpiredError,
    DownloadLimitReachedError,
    InvalidExpiryError,
    InvalidDownloadLimitError
)
import asyncio
from app.db.database import SessionLocal
from app.services.cleanup_service import cleanup_expired_files

app = FastAPI(title="SecureShare API")
init_db()

app.include_router(upload.router)
app.include_router(download.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "SecureShare running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "File not found"})


@app.exception_handler(LinkExpiredError)
async def link_expired_handler(request: Request, exc: LinkExpiredError):
    return JSONResponse(status_code=403, content={"detail": "Link expired"})


@app.exception_handler(DownloadLimitReachedError)
async def download_limit_handler(request: Request, exc: DownloadLimitReachedError):
    return JSONResponse(status_code=403, content={"detail": "Download limit reached"})


@app.exception_handler(InvalidExpiryError)
async def invalid_expiry_handler(request: Request, exc: InvalidExpiryError):
    return JSONResponse(status_code=400, content={"detail": "Invalid expiry value"})


@app.exception_handler(InvalidDownloadLimitError)
async def invalid_limit_handler(request: Request, exc: InvalidDownloadLimitError):
    return JSONResponse(status_code=400, content={"detail": "Invalid max_downloads value"})

@app.on_event("startup")
async def start_cleanup_job():
    async def cleanup_loop():
        while True:
            db = SessionLocal()
            try:
                cleanup_expired_files(db)
            finally:
                db.close()

            await asyncio.sleep(60)  # run every 60 seconds

    asyncio.create_task(cleanup_loop())