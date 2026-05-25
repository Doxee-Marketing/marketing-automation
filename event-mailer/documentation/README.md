# Event Mailer

Pannello RSVP per eventi Outlook, anche per destinatari Gmail e altri domini non-Microsoft.

![pannello](docs/screenshot.png)

---

## A chi serve

- Chi organizza eventi aziendali tramite calendario Microsoft 365 e deve tracciare le conferme di partecipazione.
- Chi deve invitare persone con email Gmail o altri provider che non ricevono correttamente gli inviti diretti da Outlook.
- Chi ha bisogno di esportare la lista dei partecipanti in Excel con un click.

---

## Cosa fa

- Legge in tempo reale gli stati RSVP dal calendario Microsoft Exchange (Accepted, Declined, Tentative, Pending).
- Invia inviti compatibili con Gmail, Apple Mail e qualsiasi client email: il destinatario vede i pulsanti Accetta / Rifiuta / Forse nell'email.
- Raccoglie le risposte anche da indirizzi non-Microsoft leggendole dalla inbox dell'organizzatore via API.
- Permette di aggiungere invitati nuovi direttamente dal pannello, con invio immediato dell'invito.
- Esporta la lista RSVP in un file Excel formattato (.xlsx), con filtro per stato.

---

## Requisiti

- Mac con macOS 10.15 o successivo.
- Python 3.8 o successivo (scaricabile da [python.org](https://www.python.org/downloads/)).
- Un account Microsoft 365 con accesso al calendario (es. account aziendale o scolastico).
- Un'app registrata su Azure Active Directory con i permessi corretti (vedi [INSTALL.md](INSTALL.md)).

---

## Quick start

1. Segui la guida completa in [INSTALL.md](INSTALL.md) per il primo avvio.
2. Esporta l'evento da Outlook come `evento.ics` e mettilo nella cartella `event-mailer`.
3. Fai doppio click su `start.command`.

---

## Come funziona dietro le quinte

Al primo avvio, un wizard legge automaticamente il file `.ics` nella cartella, ricava il titolo dell'evento e chiede le credenziali Azure una volta sola. Il Client Secret non viene mai scritto in un file di testo: viene salvato cifrato nel **macOS Keychain** tramite la libreria `keyring`.

Per autenticarsi con Microsoft, il programma usa il **device code flow OAuth2**: genera un codice monouso, lo copia negli appunti e apre il browser sulla pagina di login Microsoft. L'utente incolla il codice, conferma con il proprio account, e il programma riceve automaticamente il token di accesso senza che la password passi mai per il codice.

Tutti i dati RSVP vengono letti in tempo reale dalla **Microsoft Graph API**: sia dall'elenco partecipanti dell'evento Exchange, sia dalla inbox dell'organizzatore (per intercettare le risposte da indirizzi Gmail e simili che Exchange non processa automaticamente).

Il pannello si aggiorna ogni 8 secondi senza bisogno di ricaricare la pagina.

---

## Privacy e sicurezza

- Il Client Secret è salvato nel **macOS Keychain**: non finisce mai in un file di testo, non viene trasmesso a servizi terzi.
- Il file `config.json` (che contiene Tenant ID e Client ID) è elencato nel `.gitignore` e non viene incluso in eventuali commit.
- Il token di accesso Microsoft è salvato in `.token_cache.json` con permessi `chmod 600` (leggibile solo dall'utente corrente).
- Nessun dato viene inviato a server esterni al di fuori di Microsoft Graph API.

---

## Limiti noti

- Funziona solo su **Mac**: il file `start.command` e la copia automatica negli appunti (`pbcopy`) sono specifici di macOS.
- Richiede che l'app Azure abbia il **device code flow abilitato** (Public client flows: sì). Senza questa impostazione il login non funziona.
- Il pannello gira in locale sulla porta 8765: non è accessibile da altri computer sulla rete.

---

## Licenza

MIT — vedi [LICENSE](LICENSE) per il testo completo.
