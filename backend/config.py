"""
Centralised settings — loaded from environment variables / .env file.
All secrets are read here and nowhere else in the codebase.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Environment ──────────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./atsparser.db" # Default to SQLite for easy start

    # ── Redis (Celery broker + result backend) ───────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Cloudflare R2 (S3-compatible file storage) ───────────────────────────
    R2_BUCKET: str = "atsparser-resumes"
    R2_ENDPOINT: str = ""          # e.g. https://<account_id>.r2.cloudflarestorage.com
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""

    # ── Clerk (auth) ─────────────────────────────────────────────────────────
    CLERK_SECRET_KEY: str = ""     # sk_test_...
    CLERK_PUBLISHABLE_KEY: str = ""

    # ── Frontend origin (CORS) ───────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    # ── Sentry ───────────────────────────────────────────────────────────────
    SENTRY_DSN: str = ""

    # ── File limits ──────────────────────────────────────────────────────────
    MAX_UPLOAD_SIZE_MB: int = 10
    MAX_BATCH_SIZE: int = 10

    # ── Data retention (days) ────────────────────────────────────────────────
    RETENTION_DAYS: int = 30


settings = Settings()
