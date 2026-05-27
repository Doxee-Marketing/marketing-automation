# Setup Event Mailer su Windows — da zero

Guida passo-passo per installare e lanciare Event Mailer su un PC Windows aziendale senza Git né Python preinstallati.

**Tempo richiesto:** ~15 minuti. Serve solo connessione internet.

---

## 1. Installa Git per Windows

Vai su [git-scm.com/download/win](https://git-scm.com/download/win). Parte automaticamente il download di un `.exe`.

Doppio click sull'`.exe`. Wizard di installazione: clicca **Next** fino in fondo, lascia tutte le opzioni di default. Alla fine **Install**, aspetta, **Finish**.

**Verifica:** apri il **Prompt dei comandi** (tasto Windows → digita `cmd` → Invio) e lancia:

```
git --version
```

Deve uscire `git version 2.xx.x`. Se sì, vai avanti.

---

## 2. Installa Python 3

Vai su [python.org/downloads](https://www.python.org/downloads/). Click sul bottone giallo grande **Download Python 3.x.x**. Parte un altro `.exe`.

Doppio click sull'`.exe`. **STOP — non cliccare subito Install Now.**

Sulla prima schermata, in basso, c'è una casella **"Add python.exe to PATH"**. **Spuntala** prima di proseguire. Senza questa spunta non funziona niente.

Adesso click su **Install Now**. Aspetta. **Close**.

**Verifica:** **chiudi e riapri** il Prompt dei comandi (importante, il PATH si aggiorna solo nelle finestre nuove), poi:

```
python --version
```

Deve uscire `Python 3.x.x`. Se esce "non riconosciuto", la spunta PATH è saltata: rilancia l'installer Python, **Modify**, spunta la casella, **Next**, **Install**.

---

## 3. Scarica il progetto con git

Nel Prompt dei comandi, posizionati sul Desktop e clona la repo:

```
cd %USERPROFILE%\Desktop
git clone https://github.com/Doxee-Marketing/marketing-automation.git
```

Dopo qualche secondo si crea una cartella `marketing-automation` sul Desktop.

Entra dentro la cartella del progetto:

```
cd marketing-automation\event-mailer
```

---

## 4. Metti il file evento

Apri Outlook (web: [outlook.office.com](https://outlook.office.com), oppure desktop), apri l'evento del calendario, esportalo come `.ics`:

- **Outlook Web:** apri evento → tre puntini `...` in alto → **Esporta evento** → si scarica un `.ics`
- **Outlook Desktop:** apri evento → **File** → **Salva con nome** → formato **ICS**

Rinomina il file in `evento.ics` (tutto minuscolo, senza spazi) e mettilo dentro la cartella `event-mailer\ics\`.

---

## 5. Chiedi le credenziali Azure a Leo

Servono tre valori per il primo setup:

- **Tenant ID**
- **Client ID**
- **Client Secret**

Te li manda Leo via password manager aziendale o messaggio diretto Teams. Tienili pronti, ti servono tra 30 secondi.

---

## 6. Lancia il programma

Sempre nel Prompt dei comandi, dentro la cartella `event-mailer`:

```
start.bat
```

Probabile che Windows mostri **"Windows ha protetto il tuo PC"** → click **Ulteriori informazioni** → **Esegui comunque**.

Si apre una nuova finestra nera. Prima volta: installa automaticamente i pacchetti python necessari (~1 minuto). Poi parte il wizard.

**[1/3] Evento:** rileva il `.ics`, propone come keyword il titolo dell'evento. Premi **Invio** per confermare.

**[2/3] Azure:** incolla il **Tenant ID** → Invio. Incolla il **Client ID** → Invio.

**[3/3] Client Secret:** incolla il secret → Invio.

> Mentre incolli **non vedi nulla**, il cursore non si muove — è normale, il testo è nascosto per sicurezza. Premi Invio dopo aver incollato.

Quando vedi `Setup completato.`, il wizard ha finito.

---

## 7. Login Microsoft

Subito dopo il setup parte il login Microsoft. Vedi qualcosa tipo:

```
Codice: ABC-DEF (già copiato negli appunti)
Pagina: https://login.microsoftonline.com/common/oauth2/deviceauth
```

Il browser si apre automaticamente sulla pagina Microsoft. Il codice è già negli appunti, click sul campo testo e **Ctrl+V** → Next.

Login con email Doxee + password. Conferma i permessi richiesti.

Torna alla finestra nera. Quando vedi `Login confermato.`, sei dentro.

Il browser si apre automaticamente su `http://localhost:8765` → dashboard live. Funziona.

---

## 8. Uso quotidiano

Dalla seconda volta in poi: doppio click su `start.bat` dentro la cartella `event-mailer`. Niente wizard, niente login, la dashboard parte diretta.

Per fermare il programma: chiudi la finestra nera, oppure `Ctrl+C` dentro quella finestra.

---

## Se qualcosa si rompe

**`start.bat` si chiude subito senza messaggi.**
Python non è in PATH. Riapri l'installer Python → **Modify** → spunta **"Add Python to PATH"** → Next → Install.

**`pip install` fallisce con timeout o "could not fetch".**
Proxy aziendale che blocca. Apri il Prompt dei comandi nella cartella `event-mailer` e lancia (sostituendo `PROXY:PORTA` con i valori che ti dà l'IT):

```
python -m pip install --user --proxy http://PROXY:PORTA -r automation\requirements.txt
```

**Antivirus blocca `start.bat`.**
Succede su CrowdStrike, Defender for Endpoint, Sophos. IT deve whitelistare la cartella `event-mailer`.

**"Nessun evento '...' trovato su Exchange".**
La keyword in `config.json` non matcha il titolo dell'evento su Outlook. Apri `automation\config.json` con Blocco note, cambia `event_keyword` con una parola del titolo esatto, salva, rilancia `start.bat`.

**"Porta 8765 già in uso".**
C'è già una finestra del programma aperta. Chiudila e rilancia. Per forzare la chiusura:

```
netstat -ano | findstr :8765
taskkill /PID <PID> /F
```

Dove `<PID>` è il numero che vedi nell'ultima colonna del comando precedente.

**Client Secret scaduto o revocato.**
Cancella `.token_cache.json` e `automation\config.json` dalla cartella `event-mailer`. Rilancia `start.bat`: il wizard riparte e puoi inserire il nuovo secret.
