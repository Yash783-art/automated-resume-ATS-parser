from celery import Celery
from backend.config import settings

celery_app = Celery(
    "atsparser",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["backend.tasks.parse", "backend.tasks.match", "backend.tasks.cleanup"]
)

import os

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "cleanup-expired-resumes-daily": {
            "task": "backend.tasks.cleanup.cleanup_expired_resumes",
            "schedule": 86400.0, # Once a day
        },
    },
)

# If REDIS_URL is not set or Redis is unavailable, run tasks synchronously
if not os.getenv("REDIS_URL"):
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_eager_propagates = True
