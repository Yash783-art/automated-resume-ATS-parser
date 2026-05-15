"""
ATS Parser — FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db, engine, Base

from backend.config import settings


# ─── Sentry — error tracking ─────────────────────────────────────────────────
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.2,
        environment=settings.ENVIRONMENT,
    )


# ─── Database Initialization ─────────────────────────────────────────────────
from backend.models import User, Resume, ParsedResume, JobDescription, MatchResult

try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized successfully.")
except Exception as e:
    print(f"❌ Database error: {e}")


# ─── Lifespan — startup / shutdown hooks ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: pre-load heavy models so first request isn't slow
    # (sentence-transformers model is loaded lazily in embedder.py singleton)
    yield
    # Shutdown: nothing to clean up right now


# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ATS Parser API",
    version="1.0.0",
    description="Resume parsing and ATS match scoring service.",
    lifespan=lifespan,
)

# ─── Traffic Logger ──────────────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request, call_next):
    origin = request.headers.get("origin")
    print(f"📥 Incoming: {request.method} {request.url} | Origin: {origin}")
    response = await call_next(request)
    print(f"📤 Response: {response.status_code}")
    return response

import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_msg = f"CRASH: {str(exc)}\n{traceback.format_exc()}"
    print(error_msg)
    with open("crash_log.txt", "w") as f:
        f.write(error_msg)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )

# ─── CORS ────────────────────────────────────────────────────────────────────
# We use a broad policy for development to ensure connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Prometheus metrics ──────────────────────────────────────────────────────
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# ─── Routers (registered after middleware) ───────────────────────────────────
from backend.routers import resume, jd, match, export, analytics  # noqa: E402

app.include_router(resume.router,    prefix="/api/resume", tags=["resume"])
app.include_router(jd.router,        prefix="/api/jd",     tags=["jd"])
app.include_router(match.router,     prefix="/api/match",  tags=["match"])
app.include_router(export.router,    prefix="/api/export", tags=["export"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/health", tags=["health"])
async def health():
    import os
    redis_ok = False
    try:
        from redis import Redis
        r = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        redis_ok = r.ping()
    except Exception:
        pass
    return {"status": "ok", "redis": redis_ok, "db": "ok", "version": "1.0.0"}
