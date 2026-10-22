@echo off
echo ===================================================
echo Starting Financial Parallelverse - FastAPI Backend
echo Port: 8000 | Docs: http://localhost:8000/api/docs
echo ===================================================
cd /d "%~dp0"
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
