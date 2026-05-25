@echo off
REM Launcher Windows — doppio click su questo file per avviare l'app.
REM Crea il virtualenv al primo avvio, poi lancia Streamlit nel browser.

cd /d %~dp0

if not exist .venv (
    echo [setup] Creazione virtualenv (una tantum, ~1 minuto)...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [run] Avvio app — si apre nel browser su http://localhost:8501
streamlit run app.py
pause
