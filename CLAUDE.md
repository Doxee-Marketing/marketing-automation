# CLAUDE.md — Doxee Marketing AI

Repo di automazioni marketing di Doxee. Costruito da Leonardo Bellani (aprile–giugno 2026).

---

## Struttura del repo

```
doxee-marketing-ai/
├── leadcleaner/       # Node.js — web app XLSX → Apollo enrichment → scoring
├── deal-engagement/   # Python — HubSpot deals → Excel report
├── event-mailer/      # Python — RSVP dashboard Outlook + inviti cross-client
└── README-TEMPLATE.md # Template standard per nuove automazioni
```

Ogni automazione è indipendente e ha il proprio README, stack e variabili d'ambiente.

---

## Stack per progetto

| Progetto | Runtime | Dipendenze chiave | Secrets |
|---|---|---|---|
| `leadcleaner` | Node.js | Express, xlsx, axios | `APOLLO_API_KEY` in `.env` |
| `deal-engagement` | Python 3.8+ | requests, openpyxl, streamlit, PyYAML | `HUBSPOT_TOKEN` in `src/.env` |
| `event-mailer` | Python 3.8+ | Microsoft Graph API, icalendar, openpyxl | Azure AD app credentials in `config.json` |

---

## Prima di toccare qualsiasi codice

1. Leggi il README della cartella specifica — contiene il flusso, i parametri configurabili e i vincoli.
2. Copia sempre `.env.example` → `.env` (o `config.example.json` → `config.json`). Non committare mai file con credenziali reali.
3. Non modificare `usage.json` in `leadcleaner/` — è il contatore delle chiamate Apollo, viene gestito dal server.

---

## Vincoli importanti

**Apollo (LeadCleaner)**
- Il piano attivo ha un limite mensile di crediti configurato in `APOLLO_MONTHLY_LIMIT` (default: 30.020).
- Il contatore locale (`usage.json`) traccia solo le chiamate fatte via LeadCleaner. Se Apollo viene usato anche da altri strumenti, il saldo reale nel dashboard Apollo sarà più basso.
- L'endpoint di arricchimento è `POST /people/match` — consuma un credito anche se non trova match.
- Gestisci sempre il caso 429 (`quota exhausted`) prima di fare batch grandi.

**HubSpot (Deal Engagement)**
- L'app è read-only: non scrive mai nulla su HubSpot.
- Il token è un Private App token (prefisso `pat-eu1-...`). Scopi necessari: `crm.lists.read`, `crm.objects.deals.read`, `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.associations.read`.
- I dati storici pre-aprile 2026 non sono sincronizzati con Salesforce.
- La cache è in `src/data/cache/`. Tienila aggiornata disabilitando il flag quando servono dati freschi.

**Microsoft Graph (Event Mailer)**
- Richiede un'app Azure AD registrata con i permessi corretti (vedi `automation/INSTALL.md`).
- Le risposte RSVP da Gmail e client non-Microsoft vengono lette dall'inbox dell'organizzatore via API, non dalla notifica Exchange diretta.

---

## Scoring lead (LeadCleaner)

La logica è in `leadcleaner/src/services/scoring.js`. Range: -15 → +25.

| Condizione | Punti |
|---|---|
| Job title in lista target (C-level, IT leadership) | +5 |
| Job title negativo (Student, HR) | -15 |
| Industry in lista target (Banking, Telco, IT Services…) | +10 |
| Company size ≥ 500 dipendenti | +5 |

Per aggiornare le liste, modifica `TARGET_TITLES`, `NEGATIVE_TITLES`, `TARGET_INDUSTRIES` direttamente in quel file.

---

## Deal Engagement — parametri principali

| Parametro | Valori comuni |
|---|---|
| `list_id` | `17621` (opp. 2026) / `17603` (mese corrente) |
| `score_property` | `lead_score_contacts_total` / `lead_score_contacts_engagement` |
| `score_threshold` | `null` esclude solo i non-scorati; `5` → solo Medium+High |

Configurazione in `deal-engagement/src/config.yaml`.

---

## Aggiungere una nuova automazione

1. Crea una nuova cartella nella root.
2. Copia `README-TEMPLATE.md` e compilalo.
3. Aggiungi la riga nella tabella del README principale.
4. Aggiungi un `start.command` per Mac se è un'app locale.
5. Aggiungi sempre un `.env.example` / `config.example.json` — mai file con credenziali reali.

---

## Contatti

Leonardo Bellani — lbellani@doxee.com  
Emanuela Disperati — edisperati@doxee.com  
Ref: Judith Schuder (Marketing)
