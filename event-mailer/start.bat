@echo off
cd /d "%~dp0"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRORE] Python non trovato.
    echo Installalo da https://www.python.org/downloads/
    echo IMPORTANTE: durante l'installazione spunta "Add Python to PATH".
    pause
    exit /b 1
)
python -c "import requests, openpyxl, keyring" >nul 2>&1
if %errorlevel% neq 0 (
    echo [setup] Installo le dipendenze...
    python -m pip install --user -q -r automation\requirements.txt
    if %errorlevel% neq 0 (
        echo [ERRORE] Installazione dipendenze fallita.
        echo Prova manualmente: python -m pip install --user -r automation\requirements.txt
        pause
        exit /b 1
    )
)
python automation\server.py
if %errorlevel% neq 0 (
    echo.
    pause
)
