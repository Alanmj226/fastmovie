@echo off
echo Copying Fast Movie logo...
powershell -Command "Copy-Item 'C:\Users\Alan\.gemini\antigravity\brain\876678af-7fea-4fc2-8621-f23503c45131\fast_movie_logo_v2_1778080895874.png' -Destination 'd:\VSC\.vscode\logo.png' -Force"
if exist "d:\VSC\.vscode\logo.png" (
    echo.
    echo SUCCESS! logo.png has been created.
    echo Refresh your browser to see the new logo.
) else (
    echo.
    echo FAILED - Could not copy logo file.
)
echo.
pause
