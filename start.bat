@echo off
set ECHO_OS=windows
title Echo's Hacking Game - Der Erbschafts-Coup
color 0A

echo.
echo ================================================
echo    ECHO'S HACKING GAME - DER ERBSCHAFTS-COUP
echo ================================================
echo.
echo Willkommen zum ultimativen Hacking-Lernspiel!
echo.
echo [INFO] Starte das Spiel...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Python ist nicht installiert!
    echo.
    echo Bitte installiere Python von: http://www.python.org/downloads/
    echo Stelle sicher, dass "Add Python to PATH" aktiviert ist!
    echo.
    pause
    exit /b 1
)

REM Validate virtual environment integrity
set VENV_OK=0
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -V >nul 2>&1
    if %errorlevel% equ 0 set VENV_OK=1
)

if %VENV_OK% neq 1 (
    echo [INFO] Erstelle Virtual Environment...
    if exist ".venv" rmdir /s /q .venv
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [FEHLER] Virtual Environment konnte nicht erstellt werden!
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Aktiviere Virtual Environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [FEHLER] Virtual Environment konnte nicht aktiviert werden!
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Installiere Dependencies...
pip install flask requests
if %errorlevel% neq 0 (
    echo [WARNUNG] Dependencies konnten nicht installiert werden!
    echo Das Spiel wird trotzdem versucht zu starten...
)

REM Check if game file exists
if not exist "hacking_game.py" (
    echo [FEHLER] hacking_game.py nicht gefunden!
    echo Bitte stelle sicher, dass alle Dateien im richtigen Ordner sind.
    pause
    exit /b 1
)

REM Start the game
echo.
echo [INFO] Starte Echo's Hacking Game...
echo.
echo ================================================
echo    VIELE ERFOLG BEIM ERBSCHAFTS-COUP!
echo ================================================
echo.

python hacking_game.py

REM If game exits, show message
echo.
echo ================================================
echo    SPIEL BEENDET
echo ================================================
echo.
echo Danke fürs Spielen! Echo wird dich vermissen...
echo.
pause