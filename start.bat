@echo off
REM CropGuard AI 1-Click Startup Script for Windows
echo ========================================================
echo   Starting CropGuard AI Multilingual Agricultural Engine
echo ========================================================

IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat 2>nul || (
    echo Using system python...
)

echo Installing / verifying requirements...
pip install -r requirements.txt

echo.
echo Launching CropGuard AI on http://127.0.0.1:8000
echo Swagger UI Docs available at http://127.0.0.1:8000/docs
echo.
python -m uvicorn Backend.app:app --host 0.0.0.0 --port 8000 --reload
pause
