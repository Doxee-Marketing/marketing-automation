# INSTALL — Guida all'installazione

Questa guida ti porta dall'azzeramento totale al primo invito inviato, passo dopo passo.
Non serve nessuna competenza tecnica.

---

## 1. Cosa ti serve prima di iniziare

- Un Mac (questa guida non funziona su Windows o Linux).
- Un account Microsoft 365 con accesso al calendario (es. account aziendale).
- Accesso al portale Azure della tua organizzazione per registrare l'app (o qualcuno che lo faccia per te, vedi sezione 4).
- Connessione internet.

---

## 2. Installare Python 3

Vai su [https://www.python.org/downloads/](https://www.python.org/downloads/).

Clicca sul grande pulsante giallo **Download Python 3.x.x**. Si scarica un file `.pkg`.

Fai doppio click sul file scaricato e segui il wizard: **Continua → Continua → Accetta → Installa**.

Per verificare che sia andato a buon fine, apri il **Terminale** (cercalo con Spotlight: `Cmd+Spazio`, scrivi `Terminale`, premi Invio) e scrivi:

```
python3 --version
```

Premi Invio. Dovresti vedere qualcosa come `Python 3.12.3`. Se compare una versione, Python è installato correttamente.

---

## 3. Scaricare il progetto

**Opzione A — con Git (se lo hai installato):**

Apri il Terminale e scrivi:

```
git clone https://github.com/TUO-UTENTE/event-mailer.git
```

Poi:

```
cd event-mailer
```

**Opzione B — scaricando lo ZIP:**

Vai sulla pagina GitHub del progetto. Clicca su **Code** (pulsante verde in alto a destra). Clicca su **Download ZIP**.

Apri il file `.zip` scaricato: si crea una cartella `event-mailer`. Spostala dove preferisci (es. sul Desktop).

---

## 4. Registrare l'app su Azure

Questo passaggio serve per ottenere le credenziali che il programma usa per accedere al calendario Microsoft. Va fatto una volta sola.

> Se nella tua organizzazione non hai i permessi per registrare app su Azure, chiedi all'amministratore IT di seguire questi passi e di darti i tre valori finali: Tenant ID, Client ID e Client Secret.

**4.1 — Apri il portale Azure**

Vai su [https://portal.azure.com](https://portal.azure.com) e accedi con il tuo account Microsoft 365.

**4.2 — Vai su App Registrations**

Nella barra di ricerca in cima, scrivi `App registrations`. Clicca sul risultato **App registrations**.

**4.3 — Crea una nuova app**

Clicca su **+ New registration** (in alto a sinistra).

Nel campo **Name** scrivi un nome qualsiasi, per esempio `event-mailer`.

Sotto **Supported account types** seleziona **Accounts in this organizational directory only**.

Lascia tutto il resto com'è. Clicca **Register**.

Sei ora nella pagina della tua app. Troverai due valori importanti:

- **Application (client) ID** → copialo e salvalo da qualche parte.
- **Directory (tenant) ID** → copialo e salvalo da qualche parte.

![screenshot placeholder — pagina overview app Azure](docs/azure-overview.png)

**4.4 — Abilita il device code flow**

Nel menu a sinistra, clicca su **Authentication**.

Clicca su **+ Add a platform**. Seleziona **Mobile and desktop applications**.

Spunta la casella `https://login.microsoftonline.com/common/oauth2/nativeclient`. Clicca **Configure**.

Torna alla pagina **Authentication**. Scorri in basso fino a **Advanced settings**. Imposta **Allow public client flows** su **Yes**. Clicca **Save**.

**4.5 — Aggiungi i permessi**

Nel menu a sinistra, clicca su **API permissions**.

Clicca su **+ Add a permission**. Seleziona **Microsoft Graph**. Seleziona **Delegated permissions**.

Cerca e spunta questi cinque permessi:

- `Calendars.ReadWrite`
- `Mail.Read`
- `Mail.Send`
- `User.Read`
- `offline_access`

Clicca **Add permissions**.

Clicca su **Grant admin consent for [nome organizzazione]**, poi conferma con **Yes**.

> Se non vedi questo pulsante, hai bisogno dei permessi di amministratore. Chiedi all'IT.

**4.6 — Crea il Client Secret**

Un **Client Secret** è una password generata da Microsoft per la tua app: serve a dimostrare che sei tu a usarla.

Nel menu a sinistra, clicca su **Certificates & secrets**. Clicca su **+ New client secret**.

Nel campo **Description** scrivi qualcosa tipo `event-mailer`. In **Expires** scegli **24 months** (o il massimo disponibile). Clicca **Add**.

Appare una riga con il secret. Il valore nella colonna **Value** è visibile solo adesso: **copialo subito** e salvalo in un posto sicuro. Se esci dalla pagina senza copiarlo, dovrai crearne uno nuovo.

Ora hai tutto: Tenant ID, Client ID, Client Secret.

---

## 5. Creare l'evento su Outlook e salvarlo come .ics

Crea il tuo evento normalmente su Outlook (web o desktop): imposta titolo, data, ora, descrizione.

**Da Outlook Web ([https://outlook.office.com](https://outlook.office.com)):**

Apri l'evento nel calendario. Clicca su **...** (i tre puntini in alto a destra dell'evento). Clicca su **Export event**. Si scarica un file `.ics`.

**Da Outlook Desktop (Mac):**

Apri l'evento. Dal menu in cima scegli **File → Save As**. Scegli il formato **ICS**. Clicca **Save**.

Rinomina il file scaricato in `evento.ics` (tutto minuscolo, niente spazi).

Copia `evento.ics` nella cartella `event-mailer` (quella che hai scaricato al passo 3).

---

## 6. Primo avvio

Apri la cartella `event-mailer` nel Finder.

Fai **doppio click** su `start.command`.

Si apre una finestra del Terminale. Se appare un avviso di sicurezza macOS ("impossibile aprire l'applicazione da uno sviluppatore non identificato"), vai in **Impostazioni di Sistema → Privacy e Sicurezza** e clicca **Apri comunque**.

Il programma installa le dipendenze necessarie (richiede internet, dura pochi secondi). Poi parte il wizard di configurazione.

Il wizard fa tre cose:

**[1/3] Evento:** legge il file `evento.ics` e propone automaticamente il titolo come keyword. Premi Invio per confermarlo, o scrivi una keyword diversa (una parola del titolo dell'evento) e premi Invio.

**[2/3] Azure:** il programma chiede Tenant ID e Client ID. Incolla quelli che hai copiato al passo 4 e premi Invio dopo ognuno.

**[3/3] Client Secret:** il programma chiede il Client Secret. Incollalo e premi Invio. Il cursore non si muove mentre scrivi (è normale: nasconde il testo per sicurezza). Il secret viene salvato cifrato nel macOS Keychain e non apparirà mai in nessun file.

Quando vedi `Setup completato.`, il wizard è finito.

---

## 7. Login Microsoft (device code flow)

Subito dopo il setup, il programma avvia il login Microsoft.

Vedi nel Terminale qualcosa come:

```
============================================================
  Codice:  ABC-DEF   (gia' copiato negli appunti)
  Pagina:  https://login.microsoftonline.com/common/oauth2/deviceauth
============================================================
  Ho aperto la pagina nel browser. Incolla il codice e conferma.
  Resto in attesa qui sotto...
```

Il browser si apre automaticamente sulla pagina Microsoft. Il codice è già copiato negli appunti.

Clicca nel campo di testo della pagina Microsoft e incolla il codice (`Cmd+V`). Clicca **Next**.

Accedi con il tuo account Microsoft 365 (email e password aziendali). Conferma i permessi richiesti.

Torna al Terminale. Quando vedi `Login confermato.`, il login è andato a buon fine.

Il pannello si apre automaticamente nel browser su `http://localhost:8765`.

---

## 8. Usare il pannello

**Vedere le risposte:** le card in cima mostrano il numero di Accepted, Declined, Tentative e Pending. La tabella si aggiorna in automatico ogni 8 secondi.

**Aggiungere un invitato:** compila i campi **Nome** ed **Email** nella sezione "Aggiungi invitato". Clicca **Invia invito**. Il destinatario riceve una email con l'invito iCalendar (con i pulsanti Accetta / Rifiuta / Forse, compatibili con Gmail e qualsiasi client email).

**Filtrare per stato:** clicca su una delle card colorate (Accepted, Declined, ecc.) per filtrare la tabella. Puoi selezionarne più di una. Clicca **Pulisci filtri** per toglierli.

**Esportare in Excel:** clicca il pulsante **Esporta XLSX**. Se hai un filtro attivo, il file conterrà solo i partecipanti visibili. Il file si chiama `rsvp_[stato]_[data_ora].xlsx` e viene scaricato nella cartella Download.

**Aggiornare manualmente:** clicca il pulsante **↻ Aggiorna** in alto a destra per forzare una lettura fresca da Exchange.

**Modificare lo stato di un invitato manuale:** se un invitato è stato aggiunto a mano dal pannello (e non tramite Outlook), il suo stato mostra una freccia ▾. Cliccaci sopra per cambiarlo.

---

## 9. Avvii successivi

Dal secondo avvio in poi: fai doppio click su `start.command`. Il wizard non riparte. Il login Microsoft avviene in automatico (il token viene rinnovato silenziosamente). Il pannello si apre direttamente nel browser.

Se cambi evento: sostituisci il file `evento.ics` nella cartella e cancella `config.json`. Al prossimo avvio il wizard riparte e ti chiede le nuove informazioni (le credenziali Azure rimangono nel Keychain, non devi reinserirle).

---

## 10. Se qualcosa va storto

**Il Terminale si chiude subito senza fare nulla.**
Controlla che `start.command` sia nella stessa cartella degli altri file (`server.py`, `setup.py`, ecc.). Se li hai spostati separatamente, rimettili insieme.

**"Python 3 non trovato".**
Python non è installato o non è nel PATH. Torna alla sezione 2 e reinstallalo. Dopo l'installazione, chiudi e riapri il Terminale.

**"Nessun file .ics trovato nella cartella".**
Il file dell'evento non è nella cartella `event-mailer`, oppure si chiama in modo diverso da `evento.ics`. Verifica il nome e la posizione del file.

**Il browser non si apre durante il login.**
Il programma stampa l'URL nel Terminale. Aprilo a mano copiandolo nel browser: `https://login.microsoftonline.com/common/oauth2/deviceauth`. Il codice è già negli appunti: incollalo lì.

**"Accesso negato dall'utente" o errore di permessi Azure.**
I permessi dell'app non sono stati concessi correttamente (sezione 4.5). Torna sul portale Azure, controlla che tutti e quattro i permessi siano presenti e che il consenso admin sia stato concesso (voce "Granted" nella colonna Status).

**"Porta 8765 già in uso".**
C'è già una finestra di `start.command` aperta. Chiudi il Terminale precedente (o premi `Ctrl+C` in quella finestra) prima di riaprirlo.

**Il Client Secret è scaduto o è stato revocato.**
Cancella `.token_cache.json` dalla cartella `event-mailer`. Cancella `config.json`. Riavvia `start.command`: il wizard riparte e potrai inserire il nuovo secret.

**"Nessun evento con '...' nel titolo trovato su Exchange".**
La keyword configurata non corrisponde al titolo dell'evento nel calendario. Apri `config.json` e modifica il valore di `event_keyword` con una parola del titolo esatto dell'evento come appare in Outlook.
