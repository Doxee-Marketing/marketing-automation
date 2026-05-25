# [Nome Automazione] — Doxee Marketing

> Una riga che spiega cosa fa. Esempio: "Carica un file Excel di lead, li arricchisce con Apollo e restituisce un file pronto per HubSpot."

---

## Indice

- [Per chi non usa il terminale](#-per-chi-non-usa-il-terminale)
- [Per sviluppatori](#-per-sviluppatori)
- [Configurazione](#️-configurazione)
- [Problemi comuni](#-problemi-comuni)

---

## 🟢 Per chi non usa il terminale

Segui questi passi nell'ordine. Se qualcosa non funziona, vai alla sezione [Problemi comuni](#-problemi-comuni).

---

### Passo 1 — Scarica GitHub Desktop

GitHub Desktop ti permette di scaricare il progetto senza usare il terminale.

1. Vai su [desktop.github.com](https://desktop.github.com)
2. Clicca **"Download for macOS"** (o Windows)
3. Installa l'app e aprila
4. Accedi con il tuo account GitHub (o crea un account gratuito se non ce l'hai)

---

### Passo 2 — Scarica il progetto sul tuo computer

1. Apri **GitHub Desktop**
2. Nel menu in alto, clicca **File → Clone Repository**
3. Clicca sulla scheda **URL**
4. Incolla questo indirizzo:
   ```
   https://github.com/doxee/[nome-repo]
   ```
5. Scegli dove salvarlo sul tuo computer (es. `Documenti/doxee/`)
6. Clicca **Clone**

Aspetta qualche secondo. Quando finisce, il progetto è sul tuo PC.

---

### Passo 3 — Installa i prerequisiti

> Fai questo solo la prima volta.

**[PLACEHOLDER — personalizza per ogni automazione]**

Esempio per Python:
1. Vai su [python.org/downloads](https://www.python.org/downloads/)
2. Clicca il bottone giallo **"Download Python 3.x.x"**
3. Apri il file scaricato e segui l'installazione
   - ⚠️ **Importante:** spunta la casella **"Add Python to PATH"** durante l'installazione

Esempio per Node.js:
1. Vai su [nodejs.org](https://nodejs.org/)
2. Clicca **"LTS"** (la versione stabile)
3. Installa normalmente

---

### Passo 4 — Configura le credenziali

Il progetto ha bisogno di alcune chiavi API per funzionare. Non sono incluse nel download per sicurezza.

1. Apri la cartella del progetto (da GitHub Desktop: **Repository → Show in Finder**)
2. Trova il file `config.example.json`
3. Fai una copia e rinominala `config.json`
4. Apri `config.json` con un editor di testo (es. TextEdit su Mac, Blocco Note su Windows)
5. Sostituisci i valori tra virgolette con le tue credenziali:

```json
{
  "api_key": "INSERISCI_LA_TUA_CHIAVE_QUI",
  "altra_chiave": "INSERISCI_QUESTO"
}
```

> Non sai dove trovare le chiavi? Chiedi a **[NOME REFERENTE]**.

---

### Passo 5 — Avvia il programma

1. Apri la cartella del progetto in Finder
2. Fai **doppio click** sul file `Avvia.command`
3. Se appare un avviso di sicurezza: clicca **tasto destro → Apri → Apri**
4. Si aprirà una finestra nera — è normale. Aspetta che finisca.
5. **[DESCRIVI COSA SUCCEDE: es. "Apri il browser su http://localhost:3000" oppure "Il file di output si trova nella cartella output/"]**

---

### Aggiornare il programma (quando esce una nuova versione)

1. Apri **GitHub Desktop**
2. Seleziona questo progetto dalla lista a sinistra
3. Clicca **"Fetch origin"** in alto a destra
4. Se ci sono aggiornamenti, apparirà **"Pull origin"** — clicca quello
5. Fatto. Il progetto è aggiornato.

---

## 🔧 Per sviluppatori

### Prerequisiti

- Python 3.10+ / Node.js 18+ **[adatta]**
- Git

### Setup

```bash
git clone https://github.com/doxee/[nome-repo].git
cd [nome-repo]

# Python
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Node
npm install
```

### Configurazione

```bash
cp config.example.json config.json
# Edita config.json con le tue credenziali
```

### Avvio

```bash
# [INSERISCI IL COMANDO PER AVVIARE]
python main.py
# oppure
npm start
```

### Struttura del progetto

```
[nome-repo]/
├── README.md
├── .gitignore
├── config.example.json     ← template credenziali (committato)
├── config.json             ← credenziali reali (NON committato)
├── requirements.txt        ← dipendenze Python
├── Avvia.command           ← launcher doppio-click per Mac
└── src/
    └── ...
```

### Contribuire

1. Crea un branch: `git checkout -b feat/nome-modifica`
2. Fai le modifiche
3. Commit: `git commit -m "feat: descrizione"`
4. Push: `git push origin feat/nome-modifica`
5. Apri una Pull Request su GitHub

---

## ⚙️ Configurazione

| Chiave | Descrizione | Dove trovarla |
|---|---|---|
| `api_key` | Chiave API di [servizio] | [Dove trovarla] |
| `altra_chiave` | [Descrizione] | [Dove trovarla] |

---

## 🚨 Problemi comuni

**Il file `.command` non si apre / "impossibile verificare lo sviluppatore"**  
→ Fai tasto destro sul file → clicca **Apri** → clicca di nuovo **Apri** nella finestra che appare.

**"Python non trovato" o "command not found"**  
→ Python non è installato, o non è stato aggiunto al PATH durante l'installazione. Reinstalla Python e assicurati di spuntare **"Add Python to PATH"**.

**"Errore di autenticazione" / "Invalid API key"**  
→ Controlla che `config.json` esista (non `config.example.json`) e che le chiavi siano inserite correttamente, senza spazi extra.

**La finestra nera si apre e si chiude subito**  
→ C'è un errore. Apri il **Terminale** (cerca "Terminale" su Mac), trascina il file `Avvia.command` nella finestra, premi Invio. Vedrai il messaggio di errore.

**[AGGIUNGI ALTRI ERRORI SPECIFICI DI QUESTA AUTOMAZIONE]**

---

## Contatti

Problemi? Scrivi a **Leonardo Bellani** — lbellani@doxee.com  
Team Marketing Doxee
