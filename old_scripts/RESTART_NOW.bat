@echo off
title Fast Movie - SYSTEM FIX
color 0B
echo.
echo  ========================================
echo    FAST MOVIE - ULTIMATE SERVER FIX
echo  ========================================
echo.
echo  [1/3] Closing old server processes...
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im node.exe /t >nul 2>&1
echo  DONE.
echo.
echo  [2/3] Checking environment...
python --version
echo.
echo  [3/3] Starting server.py...
echo  (Wait for it to say "Server Starting")
echo  ----------------------------------------
echo.
start "Fast Movie Server" python server.py
echo.
echo  ========================================
echo    FIX COMPLETE!
echo    Wait 3 seconds and refresh your site.
echo  ========================================
echo.
pause
