@echo off
set ECHO_OS=windows
title Echo's Hacking Game
color 0A

echo.
echo ================================================
echo    ECHO'S HACKING GAME - DER ERBSCHAFTS-COUP
echo ================================================
echo.
echo Starte das Spiel...
echo.

REM Simple start - use virtual environment if available
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe hacking_game.py
) else (
    python hacking_game.py
)

echo.
echo Spiel beendet. Drücke eine beliebige Taste...
pause >nul