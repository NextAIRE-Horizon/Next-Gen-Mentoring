@echo off
REM Launch the local Next-Air-Assistant chat. Stays in this folder (zip-safe).
title Next-Air-Assistant
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo Python is not on PATH. Install Python 3.11 or 3.12, then run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create a virtual environment.
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo pip install failed.
        pause
        exit /b 1
    )
) else (
    ".venv\Scripts\python.exe" -c "import langchain" >nul 2>&1
    if errorlevel 1 (
        echo Updating packages for LangChain ...
        ".venv\Scripts\python.exe" -m pip install -r requirements.txt
        if errorlevel 1 (
            echo pip install failed.
            pause
            exit /b 1
        )
    )
)

if not exist ".env" (
    copy /Y ".env.example" ".env" >nul
    echo Created .env from .env.example.
    echo Open .env and paste OPENROUTER_API_KEY from exercise 2, then run this file again.
    notepad ".env"
    pause
    exit /b 1
)

findstr /C:"OPENROUTER_API_KEY=sk-" ".env" >nul
if errorlevel 1 (
    echo OPENROUTER_API_KEY still looks empty in .env. Paste the key from exercise 2.
    notepad ".env"
    pause
    exit /b 1
)

set "PY=%~dp0.venv\Scripts\python.exe"
echo.
echo Next-Air-Assistant is starting on http://localhost:8000
echo The first load often takes 20 to 40 seconds. That is Python waking up, not a crash.
echo Keep this window open. A browser tab opens when the page answers, not before.
echo Close this window to stop the assistant.
echo.
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for ($i=0; $i -lt 90; $i++) { Start-Sleep -Seconds 1; try { $r = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8000' -TimeoutSec 2; if ($r.StatusCode -ge 200) { Start-Process 'http://localhost:8000'; exit 0 } } catch {} }; exit 0"
"%PY%" -m chainlit run app.py -h --port 8000
pause
