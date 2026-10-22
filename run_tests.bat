@echo off
echo ===================================================
echo Running Financial Parallelverse Test Suite (Pytest)
echo ===================================================
cd /d "%~dp0"
set PYTHONPATH=.
python -m pytest backend/tests -v
pause
