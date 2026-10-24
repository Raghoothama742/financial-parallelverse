@echo off
echo ===================================================
echo Launching Complete Financial Parallelverse System
echo 1. Launching FastAPI Backend on Port 8000...
echo 2. Launching Streamlit FinTech UI on Port 8501...
echo ===================================================
cd /d "%~dp0"
start "Financial Parallelverse - FastAPI Backend" cmd /k "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
start "Financial Parallelverse - Streamlit Frontend" cmd /k "python -m streamlit run frontend_streamlit/app.py --server.port 8501"
echo.
echo Both servers have been launched in separate terminal windows!
echo Backend Docs: http://localhost:8000/api/docs
echo Streamlit App: http://localhost:8501
echo.
pause
