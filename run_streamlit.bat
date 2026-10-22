@echo off
echo ===================================================
echo Starting Financial Parallelverse - Streamlit UI
echo Port: 8501 | URL: http://localhost:8501
echo ===================================================
cd /d "%~dp0"
python -m streamlit run frontend_streamlit/app.py --server.port 8501
pause
