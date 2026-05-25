# HubSpot Deal Engagement Extractor

Estrae i deal di un segmento HubSpot e produce un Excel con account, opportunity, contatti e lead score. Un click → un file `.xlsx`. Non scrive nulla su HubSpot.

---

## Per chi deve solo usarlo — guida passo passo

> Segui questa sezione se non hai mai usato il terminale. Basta leggere in ordine.

### 1. Installa Python (solo al primo utilizzo)

1. Vai su [python.org/downloads](https://www.python.org/downloads/)
2. Clicca il pulsante giallo **"Download Python 3.x.x"**
3. Apri il file scaricato
4. **Importante (Windows):** nella prima schermata del programma di installazione, spunta la casella **"Add Python to PATH"** prima di cliccare Installa
5. Clicca Installa e aspetta che finisca
6. Chiudi il programma di installazione

### 2. Scarica questo progetto (solo al primo utilizzo)

1. Apri il Terminale (Mac: cerca "Terminale" in Spotlight con `Cmd + Spazio`) oppure il Prompt dei comandi (Windows: cerca "cmd")
2. Scegli dove mettere il progetto, ad esempio il Desktop:
   ```
   cd Desktop
   ```
3. Scarica il progetto con questo comando (copia e incolla):
   ```
   git clone https://github.com/doxee-marketing/hubspot-deal-engagement.git
   ```
4. Entra nella cartella appena creata:
   ```
   cd hubspot-deal-engagement
   ```

> Se il terminale dice `git: command not found`, installa Git da [git-scm.com/downloads](https://git-scm.com/downloads) e ripeti dal punto 1.

### 3. Configura il token HubSpot (solo al primo utilizzo)

Il token è la "chiave" che permette al programma di leggere i dati da HubSpot. Per ottenerlo:

1. Accedi a HubSpot
2. Vai in **Impostazioni** (icona ingranaggio in alto a destra)
3. Nel menu laterale: **Integrazioni → App private**
4. Clicca **"Crea app privata"**
5. Dai un nome (es. "Deal Engagement Extractor")
6. Vai nella scheda **Ambiti** e spunta:
   - `crm.lists.read`
   - `crm.objects.deals.read`
   - `crm.objects.contacts.read`
   - `crm.objects.companies.read`
   - `crm.associations.read`
7. Clicca **"Crea app"** → copia il token che appare (inizia con `pat-eu1-...`)

Ora incolla il token nel progetto:
1. Apri la cartella del progetto
2. Entra nella sottocartella `src/`
3. Cerca il file `.env.example` — se non lo vedi, attiva la visualizzazione dei file nascosti:
   - **Mac:** nel Finder premi `Cmd + Shift + .`
   - **Windows:** in Esplora File → Visualizza → spunta "Elementi nascosti"
4. Copia il file `.env.example` e rinomina la copia in `.env` (togli `.example`)
5. Apri `.env` con un editor di testo (Blocco Note su Windows, TextEdit su Mac)
6. Sostituisci `pat-eu1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` con il token che hai copiato
7. Salva e chiudi

### 4. Avvia il programma

- **Mac:** doppio click su `start.command` nella cartella principale
- **Windows:** doppio click su `src/start.bat`

**Primo avvio:** si apre una finestra nera e installa tutto il necessario. Ci vuole circa 1 minuto. Non chiuderla.

Quando vedi `You can now view your Streamlit app in your browser`, il programma è pronto. Si apre automaticamente il browser su `http://localhost:8501`.

> **Mac — messaggio di sicurezza al primo avvio:** se compare "Impossibile aprire perché proviene da uno sviluppatore non identificato", hai due opzioni:
>
> **Opzione A — da Terminale (più veloce):** apri il Terminale, entra nella cartella del progetto e lancia:
> ```
> xattr -rd com.apple.quarantine .
> ```
> Poi prova di nuovo a fare doppio click su `start.command`.
>
> **Opzione B — da Impostazioni:** vai in **Impostazioni di sistema → Privacy e sicurezza**, scorri in fondo — comparirà un avviso con il pulsante **"Apri comunque"**. Clicca lì.

### 5. Usa la dashboard

Una volta aperta la webapp nel browser, trovi una barra laterale a sinistra con tutti i parametri e il risultato al centro.

#### HubSpot List ID — quale mettere

Il List ID è il "filtro di partenza": dice allo script da quale segmento di deal partire. I due da usare normalmente sono:

| ID | Segmento |
|---|---|
| `17621` | Tutte le opportunities del 2026 |
| `17603` | Opportunities del mese corrente |

Se in futuro vuoi usare un altro segmento: vai su HubSpot → **CRM → Segments → Lists**, apri la lista che ti interessa → **Details** → in fondo alla pagina trovi il campo **ILS Segment ID**. Quel numero è il tuo List ID.

#### Score property — quale scegliere

| Property | Quando usarla |
|---|---|
| `lead_score_contacts_total` | Punteggio complessivo del contatto (default) |
| `lead_score_contacts_engagement` | Se vuoi misurare solo le attività di engagement marketing (email aperte, click, form compilati, ecc.) — equivalente alla colonna "Engagement/Activity" richiesta manualmente |

> Per capire quali contatti sono stati attivi negli ultimi mesi dal punto di vista marketing, usa `lead_score_contacts_engagement`. È la property che traccia tutte le azioni di interazione del singolo contatto.

#### Score threshold — come filtrare

Imposta la soglia minima del punteggio per far apparire un contatto nel report:

- **Lasciala a 0 (o vuota)** → compaiono tutti i contatti che hanno almeno uno score, esclusi solo quelli non ancora scorati
- **Metti 5** → solo "Medium" e "High engagement"
- **Metti 10** → solo "High engagement"

#### Cache — quando attivarla o disattivarla

La spunta **"Use local cache"** riutilizza i dati già scaricati da HubSpot (salvati in `src/data/cache/`). Questo rende il re-run molto più veloce (~3 secondi invece di ~30) e non consuma chiamate API.

- **Lasciala attiva** se stai solo cambiando soglia o property, senza bisogno di dati freschi
- **Toglila** se vuoi che lo script rilegga tutto da HubSpot (dati aggiornati al momento)

#### Genera ed esporta

1. Clicca **"Genera report"** e aspetta la progress bar
2. In alto appaiono 4 KPI: numero di deal, account, contatti engaged, pipeline totale in €
3. Sotto c'è la tabella di anteprima con tutti i dati
4. Clicca **"Scarica XLSX"** per scaricare il file

Il file viene salvato anche in `src/output/` con nome `hubspot_deal_report_<data_ora>.xlsx`.

### 6. Chiudi il programma

Chiudi la finestra del terminale/prompt dei comandi che si è aperta al punto 4.

---

## Output

`src/output/hubspot_deal_report_<YYYYMMDD_HHmm>.xlsx` — due fogli:

**Foglio 1 — Deal Report** (una riga per contatto)

| Account Name | Opportunity Name | Amount (€) | Close Date | Contact Name | Job Title | Email | Lead Score |
|---|---|---|---|---|---|---|---|

**Foglio 2 — Legend**

| Score | Fascia |
|---|---|
| ≥ 10 | High engagement |
| 5–9 | Medium engagement |
| 0–4 | Low engagement |
| — | Not yet scored |

---

## Configurazione avanzata (`src/config.yaml`)

```yaml
list_id: 17603                        # ID segmento HubSpot
score_property: lead_score_contacts_total  # property score
score_threshold: null                 # null = escludi solo non-scorati
output_dir: ./output
cache_dir: ./data/cache
```

---

## Documentazione tecnica

→ [`src/README.md`](src/README.md) — pipeline step-by-step, decisioni di design, punti aperti.

---

## Cosa non fa

- Non scrive su HubSpot
- Non si connette a Salesforce
- Non gira in automatico (nessuno scheduling)
- Non legge activities o email — il lead score è l'unico proxy di engagement
