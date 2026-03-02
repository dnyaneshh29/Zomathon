@echo off
echo ========================================
echo   Starting Causal AI Recommendation Engine
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [2/3] Starting API server...
echo Server will start at: http://localhost:8000
echo.
echo ========================================
echo   SERVER IS STARTING...
echo   Keep this window open!
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python src/api/server.py

pause
