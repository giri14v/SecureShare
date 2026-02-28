# 🔐 SecureShare — Temporary Secure File Sharing API

## 🎯 Objective

SecureShare is a production-style FastAPI backend service that enables
users to upload files and generate temporary, secure download links with
automatic expiration and access validation.

This project demonstrates real-world backend engineering practices
including:

- JWT-based authentication
- Service-layer architecture
- PostgreSQL integration
- Dockerized multi-container deployment
- Structured logging
- Background cleanup services

---

## 🚀 Core Features

- User Registration & Login
- JWT Authentication
- Secure File Upload
- Expiring Download Links
- Download Limit Enforcement
- Structured JSON Logging
- PostgreSQL Metadata Storage
- Background Cleanup Service
- Dockerized Infrastructure

---

## 🔐 Authentication System

SecureShare implements JWT (JSON Web Token) authentication using OAuth2
password flow.

### Flow

1.  User registers.
2.  User logs in via `/login`.
3.  Server validates credentials.
4.  Server generates signed JWT access token.
5.  Client includes token in `Authorization: Bearer <token>` header.
6.  Protected routes validate token before execution.

### Security Design

- Tokens are signed using SECRET_KEY.
- Tokens contain subject (user id) and expiration timestamp.
- Token verification performed on every protected route.
- Upload endpoint requires valid authentication.
- Download endpoint is token-based (public link), not JWT-based.

This separation ensures:

- Secure uploads
- Public but controlled downloads
- Clear boundary between identity auth and file access tokens

---

## 🧹 Cleanup Service

SecureShare includes an internal cleanup mechanism to manage expired
files and prevent storage bloat.

### Cleanup Responsibilities

- Identify expired file records
- Remove metadata from database
- Delete corresponding file from disk
- Log cleanup activity

### Execution Strategy

Current implementation supports:

- Validation-on-access (MVP approach)
- Optional background cleanup task (future scalable approach)

Future scalable upgrade:

- Scheduled async task
- Celery worker
- Cron-based cleanup
- Redis queue integration

This ensures long-term production readiness.

---

## 🔄 Upload Flow

1.  Authenticated user sends multipart request.
2.  File stored in uploads directory.
3.  Secure download token generated.
4.  Expiry timestamp calculated.
5.  Metadata stored in PostgreSQL.
6.  Download URL returned.

---

## 📥 Download Flow

1.  Client calls `/download/{token}`.
2.  Backend validates:
    - Token exists
    - Not expired
    - File present
    - Download count within limit
3.  If valid → stream file
4.  Else → return structured error response

---

## 🏗 Architecture

Client → FastAPI → Service Layer → PostgreSQL + File Storage

---

## 🛠 Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker & Docker Compose

---

## 📌 Future Improvements

- Cloud storage (AWS S3)
- Redis token caching
- Celery-based scheduled cleanup
- Rate limiting
- Frontend UI
- CI/CD pipeline

---
