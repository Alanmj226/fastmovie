@echo off
title Fast Movie - Python Server
color 0A
echo.
echo  ============================================
echo     FAST MOVIE - Starting Python Server...
echo  ============================================
echo.

cd /d "d:\VSC\.vscode"

echo  [1/2] Checking Python installation...
python --version
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found!
    echo  Please install Python from https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo.
echo  [2/2] Starting server.py on http://localhost:3000
echo.
echo  --------------------------------------------
echo   Server is starting... 
echo   Open browser at: http://localhost:3000
echo   Press CTRL+C to stop the server
echo  --------------------------------------------
echo.

python server.py

pause
