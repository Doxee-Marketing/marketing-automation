#!/usr/bin/env bash
# Launcher Mac — doppio click su questo file per avviare l'app.

cd "$(dirname "$0")"

VENV_PY=".venv/bin/python3"
VENV_PIP=".venv/bin/pip"
VENV_STREAMLIT=".venv/bin/streamlit"

# Controlla che python3 sia installato
if ! command -v python3 &>/dev/null; then
    echo ""
    echo "[ERRORE] Python3 non trovato."
    echo "Vai su https://www.python.org/downloads/ e installa Python, poi riprova."
    echo ""
    read -rp "Premi Invio per chiudere..."
    exit 1
fi

# Crea il virtualenv se non esiste
if [ ! -f "$VENV_PY" ]; then
    echo "[setup] Creazione virtualenv..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERRORE] Impossibile creare il virtualenv."
        read -rp "Premi Invio per chiudere..."
        exit 1
    fi
fi

# Installa le dipendenze se streamlit non è ancora presente
if [ ! -f "$VENV_STREAMLIT" ]; then
    echo "[setup] Installazione dipendenze (~1 minuto)..."
    "$VENV_PIP" install --upgrade pip --quiet
    "$VENV_PIP" install -r src/requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERRORE] Installazione dipendenze fallita. Leggi il messaggio sopra."
        read -rp "Premi Invio per chiudere..."
        exit 1
    fi
fi

echo ""
echo "[run] Avvio app — si apre nel browser su http://localhost:8501"
echo "      Per chiudere: torna qui e premi Ctrl+C"
echo ""
"$VENV_STREAMLIT" run src/app.py
