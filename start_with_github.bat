@echo off
REM GitHub Integration Complete - Restart Script
REM This script properly stops old processes and restarts the application with new features

echo.
echo ====================================================
echo   AI Project Generator - GitHub Integration Edition
echo ====================================================
echo.

REM Kill any existing Python processes
echo Stopping previous instances...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

REM Clear screen
cls

echo.
echo ====================================================
echo   AI Project Generator - Starting with GitHub Features
echo ====================================================
echo.

REM Start backend in new window
echo [1/2] Starting FastAPI Backend Server...
start "Backend Server" cmd /k "cd /d "%cd%" && python backend/main.py"

REM Wait for backend to start
echo [*] Waiting for backend to initialize...
timeout /t 5 >nul

REM Start frontend in new window
echo [2/2] Starting Streamlit Frontend...
start "Frontend UI" cmd /k "cd /d "%cd%" && streamlit run frontend/app.py --server.port=8501"

REM Wait a moment for frontend to start
timeout /t 3 >nul

echo.
echo ====================================================
echo   ✓ Application Started Successfully!
echo ====================================================
echo.
echo Backend API:        http://localhost:8000
echo API Documentation:  http://localhost:8000/api/docs
echo Frontend UI:        http://localhost:8501
echo.
echo New Features Enabled:
echo   - Edit & Update tab in UI
echo   - File editing interface
echo   - GitHub push functionality
echo   - Project update from GitHub
echo   - File content endpoints
echo.
echo Press any key to open the application...
pause

REM Open in browser
start http://localhost:8501

echo.
echo ====================================================
echo   Application is ready to use!
echo ====================================================
echo.
echo Tip: You can now:
echo   1. Generate projects
echo   2. Edit files through the UI
echo   3. Push to GitHub with one click
echo   4. Update existing GitHub projects
echo.
pause
