#!/bin/bash
# Event Mailer — doppio click per avviare.
# Tieni questa finestra del Terminale aperta finche' usi il pannello.
# Chiudila (o premi Ctrl+C) per fermare il server.

cd "$(dirname "$0")" || exit 1

# Trova Python 3
if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "[ERRORE] Python 3 non trovato."
    echo "Installalo da https://www.python.org/downloads/ e riprova."
    read -n 1 -p "Premi un tasto per chiudere..."
    exit 1
fi

# Installa dipendenze solo se mancanti
if ! "$PY" -c "import requests, openpyxl, keyring" >/dev/null 2>&1; then
    echo "[setup] Installo le dipendenze (requests, openpyxl, keyring)..."
    "$PY" -m pip install --user --quiet -r automation/requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERRORE] Installazione dipendenze fallita."
        echo "Prova manualmente: $PY -m pip install --user -r automation/requirements.txt"
        read -n 1 -p "Premi un tasto per chiudere..."
        exit 1
    fi
fi

"$PY" automation/server.py

# Se il server e' uscito con errore, tieni la finestra aperta per leggerlo.
if [ $? -ne 0 ]; then
    echo ""
    read -n 1 -p "Premi un tasto per chiudere..."
fi
