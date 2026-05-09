@echo off
title Fast Movie - Python Server
color 0A
echo.
echo  ========================================
echo    Fast Movie - Starting Python Server
echo  ========================================
echo.
cd /d "d:\VSC\.vscode"

echo  Checking Python...
python --version
if errorlevel 1 (
    echo  ERROR: Python not found! Please install Python from https://python.org
    pause
    exit
)

echo.
echo  ========================================
echo    Starting server on http://localhost:3000
echo  ========================================
echo.

:: Start Python server in background
start "Fast Movie Python Server" python server.py

:: Wait 2 seconds for server to start
timeout /t 2 /nobreak >nul

:: Open browser directly at admin page
start "" "http://localhost:3000/admin"

echo  Server is running! Press any key to STOP it.
echo  (Closing this window will stop the server)
echo.
pause

:: Kill the server when user presses a key
taskkill /f /fi "WINDOWTITLE eq Fast Movie Python Server" >nul 2>&1
echo  Server stopped.
