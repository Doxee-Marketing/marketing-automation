# Deal Engagement Extractor — HubSpot → Excel

Workflow locale che parte da un segmento di deal HubSpot e produce un Excel identico a `hubspot_deal_report.xlsx` (formato già validato): per ogni deal mostra l'account, l'opportunity, l'importo, la close date e tutti i contatti dell'account con il loro lead score.

Gira sul PC di una sola persona. Un comando, un file Excel.

---

## Output

`output/hubspot_deal_report_<YYYYMMDD_HHmm>.xlsx` con due fogli, identici al template già approvato:

**Foglio 1 — `Deal Report`** (una riga per contatto)

| Account Name | Opportunity Name | Amount (€) | Close Date | Contact Name | Job Title | Email | Lead Score |
|---|---|---|---|---|---|---|---|

Le quattro colonne deal (Account, Opportunity, Amount, Close Date) compaiono solo sulla prima riga del gruppo; i contatti successivi dello stesso deal hanno quei campi vuoti.

**Foglio 2 — `Legend`**

```
Lead Score Reference
≥ 10  →  High engagement
5–9   →  Medium engagement
0–4   →  Low engagement
—     →  Not yet scored
```

---

## Filtro applicato

Si esclude solo chi ha **score `null` / non valorizzato** (rappresentato come `—` nel template). Tutti i contatti con uno score numerico (anche 0) restano dentro: il giudizio "Low engagement" lo dà la legenda, non lo script. Soglia rialzabile da `config.yaml` se serve.

---

## Pipeline

```
[config.yaml] ──▶ run.py ──▶ data/cache/*.json ──▶ output/*.xlsx
       │                          ▲
       │                          │ HubSpot REST API (Private App token)
       └─ list_id, score_property, score_threshold
```

Step (idempotenti, ognuno cacha il proprio JSON in `data/cache/`):

1. `step1_list_memberships.json` — GET deal del segmento
2. `step2_deals_detail.json` — POST batch read deal (`dealname`, `amount`, `closedate`)
3. `step3_deal_to_companies.json` — POST associations deal → company
4. `step4_companies_detail.json` — POST batch read company (`name`, `domain`)
5. `step5_company_to_contacts.json` — POST associations company → contact (tutti i contatti dell'account)
6. `step6_contacts_detail.json` — POST batch read contact (`firstname, lastname, jobtitle, email, <score_property>`)
7. **filtro score in locale** — drop dei contatti con score `null` / `< threshold`
8. **build XLSX con openpyxl** — schema del template

I 6 JSON che hai già scaricato vanno copiati in `data/cache/` con questi nomi (mapping nel `--init` dello script). Lo script salta gli step già in cache. Per re-run pulito: `rm -rf data/cache/`.

---

## Decisioni di design

| Decisione | Scelta | Perché |
|---|---|---|
| Linguaggio | Python 3.10+ | Stack già allineato (openpyxl). |
| Token | `.env` locale | Niente commit di credenziali. |
| Caching | File JSON per step | Re-run veloci, debug pulito. |
| Soglia score | `> null` (default) | Replica esattamente il file già validato. Modificabile in config. |
| Scope contatti | `company-wide` | I 7 contatti deal-level sono troppo pochi; il file approvato usa i contatti della company. |
| Property score | `hubspotscore` | Da confermare con Robert/CRM ops. Se Doxee usa una custom property cambia in `config.yaml`. |
| Output | XLSX | Formato richiesto, leggibile da chiunque. |

---

## Come si lancia (modalità a scelta)

### Modalità A — frontend grafico (consigliata)

Doppio click su:
- **Mac**: `start.command`
- **Windows**: `start.bat`

Il primo avvio installa le dipendenze (~1 minuto). Si apre il browser su `http://localhost:8501` con un'interfaccia che ha:
- Sidebar per token, list ID, soglia score
- Pulsante "Genera report" con progress bar
- 4 KPI in alto (numero deal, account, contatti engaged, pipeline totale €)
- Pulsante per scaricare l'XLSX
- Tabella con anteprima dei dati

Per chiudere l'app: chiudi la finestra del terminale che si è aperta.

> **Mac — primo avvio**: se il sistema dice "non posso aprire perché non identificato", click destro sul file → Apri → Apri. Una sola volta, poi diventa fidato.

### Modalità B — riga di comando (per dev / scheduling)

```bash
cd "hubspot-deal-engagement"
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # incolla il token HubSpot dentro
python run.py
```

Tempo: ~30 sec da zero, ~3 sec con cache. Output: `output/hubspot_deal_report_<timestamp>.xlsx`.

---

## Token HubSpot

Settings → Integrations → Private Apps → Create app. Scope necessari:
`crm.lists.read`, `crm.objects.deals.read`, `crm.objects.contacts.read`, `crm.objects.companies.read`, `crm.associations.read`.

Si può inserire ogni volta nella sidebar dell'app **oppure** salvarlo una tantum in `.env` (copia `.env.example` e incollalo dentro). Il token non lascia mai il PC.

---

## Configurazione (`config.yaml`)

```yaml
list_id: 17603
score_property: hubspotscore   # cambiare se Doxee usa una custom property
score_threshold: null          # null = escludi solo non-scorati. Metti 1 / 5 / 10 per soglie più strette
output_dir: ./output
cache_dir: ./data/cache
```

---

## Cosa non fa (per scelta)

- Niente activities, niente lookback. Lo score è il proxy di engagement.
- Read-only su HubSpot. Nessuna scrittura.
- Niente schedule, niente n8n. Doppio click sullo script.
- Niente Salesforce sync.

---

## Punti aperti

- [ ] Confermare nome property score in HubSpot Doxee (`hubspotscore` standard vs custom)
- [ ] Validare list ID 17603 = "Deal Created in 2026 – New Logo/Cross-Sell"
- [ ] Decidere con Judith se `score_threshold` deve essere `null` (esclude solo non-scorati, come ora) o `> 0`
