@echo off
cd /d %~dp0
start "ATSParser Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000 --host 127.0.0.1"
timeout /t 3 /nobreak >nul
start "ATSParser Celery" cmd /k "celery -A backend.tasks.celery_app worker --loglevel=info -P solo"
echo Backend: http://127.0.0.1:8000/health
pause
