# Come pubblicare questa repo su GitHub

Guida step-by-step per inizializzare git e pubblicare la repo.  
Segui i passi nell'ordine. I comandi vanno eseguiti nel **Terminale** (Mac).

---

## Passo 1 — Crea la repo su GitHub

1. Vai su [github.com](https://github.com) e accedi con il tuo account (o quello aziendale Doxee).
2. Clicca **"New repository"** (tasto verde in alto a destra).
3. Configura così:
   - **Repository name:** `doxee-marketing-ai`
   - **Description:** `Automazioni AI per il team Marketing di Doxee`
   - **Visibility:** `Private` ← importante, contiene logica interna
   - **NON** spuntare "Add a README file" (lo abbiamo già)
   - **NON** aggiungere `.gitignore` da GitHub (lo abbiamo già)
4. Clicca **"Create repository"**.
5. Copia l'URL che ti mostra GitHub, tipo: `https://github.com/doxee/doxee-marketing-ai.git`

---

## Passo 2 — Apri il Terminale nella cartella giusta

```bash
cd ~/Desktop/claudione/doxee-marketing-ai
```

Verifica di essere nel posto giusto:
```bash
ls
# Dovresti vedere: README.md  .gitignore  leadcleaner/  deal-engagement/  ...
```

---

## Passo 3 — Copia le automazioni nelle sottocartelle

Sposta (o copia) i file di ogni automazione nelle rispettive cartelle.  
Esempio per leadcleaner:

```bash
cp -r ~/Desktop/claudione/leadcleaner/lead-cleaner/* ~/Desktop/claudione/doxee-marketing-ai/leadcleaner/
```

Fai lo stesso per le altre:
```bash
cp -r ~/Desktop/claudione/deal-engagement/src/* ~/Desktop/claudione/doxee-marketing-ai/deal-engagement/
cp -r ~/Desktop/claudione/event-mailer/* ~/Desktop/claudione/doxee-marketing-ai/event-mailer/
cp -r ~/Desktop/claudione/geo/* ~/Desktop/claudione/doxee-marketing-ai/geo/
```

> **ATTENZIONE prima di copiare event-mailer:** il file `automation/config.json` contiene credenziali reali.  
> È già in `.gitignore`, quindi non verrà committato — ma verificalo con `git status` prima di fare il push.

---

## Passo 4 — Inizializza git e fai il primo commit

```bash
cd ~/Desktop/claudione/doxee-marketing-ai

# Inizializza git nella cartella
git init

# Collega al remote GitHub (usa l'URL copiato al Passo 1)
git remote add origin https://github.com/doxee/doxee-marketing-ai.git

# Controlla cosa git vede (verifica che config.json NON compaia)
git status

# Aggiungi tutto
git add .

# Primo commit
git commit -m "feat: struttura iniziale repo con tutte le automazioni"

# Pubblica su GitHub
git branch -M main
git push -u origin main
```

---

## Passo 5 — Verifica che i segreti non siano stati caricati

Dopo il push, vai sulla repo GitHub e controlla manualmente:
- `event-mailer/automation/config.json` → **non deve esserci**
- `leadcleaner/lead-cleaner/usage.json` → **non deve esserci**
- Qualsiasi file `.env` → **non deve esserci**

Se qualcosa è sfuggito:
```bash
# Rimuovi il file dal tracking git (senza cancellarlo dal disco)
git rm --cached percorso/del/file.json
git commit -m "fix: rimuovi file con credenziali dal tracking"
git push
```

---

## Come aggiungere collaboratori

1. Vai sulla repo GitHub → **Settings** → **Collaborators and teams**
2. Clicca **"Add people"** e inserisci il loro username o email GitHub

Per fare il clone, i colleghi useranno:
```bash
git clone https://github.com/doxee/doxee-marketing-ai.git
```

---

## Workflow per aggiornamenti futuri

Ogni volta che modifichi un'automazione:

```bash
cd ~/Desktop/claudione/doxee-marketing-ai

git add .
git commit -m "feat: descrizione della modifica"
git push
```

Convenzione per i messaggi di commit:
- `feat:` — nuova funzionalità
- `fix:` — correzione bug
- `docs:` — aggiornamento documentazione
- `chore:` — manutenzione (dipendenze, config)

---

## Problemi comuni

**"Permission denied" al push**  
→ Devi autenticarti. GitHub usa token personali al posto della password.  
Vai su GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token.  
Seleziona scope `repo`. Usa il token come password quando Git te la chiede.

**"remote origin already exists"**  
```bash
git remote set-url origin https://github.com/doxee/doxee-marketing-ai.git
```

**Git non è installato**  
```bash
# Su Mac con Homebrew
brew install git
```
