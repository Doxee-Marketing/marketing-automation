# Come creare e pubblicare una repo su GitHub (org Doxee)

Guida per pubblicare ogni automazione come repo separata sull'organizzazione Doxee.  
Da ripetere una volta per ogni progetto.

---

## Prima di iniziare

Assicurati di avere:
- **Accesso all'organizzazione Doxee su GitHub** — se non ce l'hai, chiedi a IT di aggiungerti
- **GitHub Desktop** installato ([desktop.github.com](https://desktop.github.com))
- I file del progetto pronti sul tuo computer

---

## Passo 1 — Crea la repo sull'organizzazione Doxee

1. Vai su [github.com/doxee](https://github.com/doxee) (accedi se serve)
2. Clicca il tasto verde **"New"** in alto a destra
3. Compila così:

   | Campo | Valore |
   |---|---|
   | **Owner** | `doxee` ← IMPORTANTE, non il tuo nome |
   | **Repository name** | es. `doxee-leadcleaner` |
   | **Description** | Una riga che spiega cosa fa |
   | **Visibility** | `Private` |
   | **Add a README** | ❌ Non spuntare |
   | **Add .gitignore** | ❌ Non spuntare |

4. Clicca **"Create repository"**
5. Copia l'URL della repo (tipo `https://github.com/doxee/doxee-leadcleaner.git`)
6. https://github.com/Doxee-Marketing/marketing-automation.git

---

## Passo 2 — Prepara la cartella del progetto

Prima di caricare su GitHub, la cartella del progetto deve avere questa struttura minima:

```
doxee-leadcleaner/       ← nome della cartella = nome della repo
├── README.md            ← obbligatorio (usa il template)
├── .gitignore           ← obbligatorio (usa quello che abbiamo)
├── config.example.json  ← template credenziali SENZA valori reali
└── [resto del codice]
```

> **config.json NON deve essere presente** (o deve essere nel .gitignore).  
> Controlla che `config.example.json` abbia solo valori placeholder tipo `"INSERISCI_QUI"`.

---

## Passo 3 — Carica il progetto con GitHub Desktop

1. Apri **GitHub Desktop**
2. Menu in alto: **File → Add Local Repository**
3. Clicca **"Choose..."** e seleziona la cartella del progetto
   - Se dice "not a git repository" clicca **"create a repository"** e poi **"Add repository"**
4. In basso a sinistra, scrivi un messaggio nel campo **"Summary"**: `primo commit`
5. Clicca il bottone blu **"Commit to main"**
6. In alto a destra apparirà **"Publish repository"** — clicca
7. Nella finestra che si apre:
   - **Name:** lascia il nome della cartella
   - **Organization:** seleziona `doxee`
   - **Keep this code private:** ✅ spuntato
8. Clicca **"Publish Repository"**

Il progetto è ora su GitHub.

---

## Passo 4 — Verifica che i segreti non siano stati caricati

Questo è il passo più importante. Vai sulla pagina GitHub della repo e controlla manualmente:

- `config.json` → **NON deve esserci**
- `.env` → **NON deve esserci**
- Qualsiasi file con password, token, chiavi API → **NON deve esserci**

Cosa cercare: file che contengono valori reali tipo `"sk-proj-..."`, `"Bearer eyJ..."`, password vere.

Se hai caricato per errore un file con credenziali: **cambia subito le credenziali** (il token compromesso va revocato) e poi contatta IT.

---

## Passo 5 — Aggiungi i collaboratori

1. Vai sulla repo GitHub
2. Clicca **Settings** (in alto a destra nella repo)
3. Menu a sinistra: **Collaborators and teams**
4. Clicca **"Add people"** o **"Add teams"**
5. Cerca il nome GitHub del collega o del team IT
6. Scegli il ruolo:
   - **Read** — può solo vedere e scaricare (per chi deve solo usarlo)
   - **Write** — può anche modificare (per chi contribuisce al codice)

---

## Come i colleghi scaricano il progetto

Manda a chi deve usarlo questo messaggio tipo:

> Ciao! Per scaricare [Nome Automazione] sul tuo computer:
> 1. Scarica e installa GitHub Desktop: https://desktop.github.com
> 2. Apri GitHub Desktop → File → Clone Repository → URL
> 3. Incolla: `https://github.com/doxee/[nome-repo]`
> 4. Scegli dove salvarlo e clicca Clone
> 5. Poi segui il README nella cartella scaricata

---

## Repo da creare (checklist)

| Repo | Stato | URL |
|---|---|---|
| `doxee-leadcleaner` | ⬜ da creare | — |
| `doxee-deal-engagement` | ⬜ da creare | — |
| `doxee-event-mailer` | ⬜ da creare | — |
| `doxee-geo` | ⬜ da creare | — |
| `doxee-kpi-tracker` | ⬜ da creare | — |
| `doxee-pptx-chatbot` | ⬜ da creare | — |
| `doxee-marketing-ai` (hub) | ⬜ da creare | — |

---

## Aggiornare una repo dopo modifiche

Ogni volta che modifichi i file localmente:

1. Apri **GitHub Desktop**
2. Seleziona la repo dalla lista a sinistra
3. Vedrai i file modificati elencati — controlla che siano giusti
4. Scrivi un messaggio nel campo **"Summary"** (es. `fix: aggiornato script Apollo`)
5. Clicca **"Commit to main"**
6. Clicca **"Push origin"** in alto a destra

I colleghi la prossima volta che aprono GitHub Desktop vedranno il pulsante **"Pull origin"** e potranno aggiornarsi.

---

## Naming convention per le repo

| Progetto | Nome repo |
|---|---|
| LeadCleaner | `doxee-leadcleaner` |
| Deal Engagement | `doxee-deal-engagement` |
| Event Mailer | `doxee-event-mailer` |
| GEO Monitor | `doxee-geo` |
| KPI Tracker | `doxee-kpi-tracker` |
| PPTX Chatbot | `doxee-pptx-chatbot` |
| Hub (indice) | `doxee-marketing-ai` |

Prefisso `doxee-` su tutto: così sono riconoscibili nell'org GitHub e nei clone locali.
