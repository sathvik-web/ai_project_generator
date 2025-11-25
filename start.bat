@echo off
REM Quick start script for AI Project Generator on Windows

echo.
echo ====================================================
echo   AI Project Generator - Quick Start
echo ====================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Install Python 3.11+ and add to PATH.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Check .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found
    echo Creating .env from template...
    copy .env.example .env >nul 2>&1
    echo IMPORTANT: Edit .env and add your GitHub token for full functionality
)

echo.
echo ====================================================
echo Starting AI Project Generator...
echo ====================================================
echo.

echo Starting Backend on http://localhost:8000
echo.

python backend/main.py

pause
