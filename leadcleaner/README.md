# Lead Cleaner - Complete Documentation

**A lead enrichment & data cleaning webapp** powered by Apollo.io API.

## Quick Start

```bash
# 1. Install dependencies
cd lead-cleaner
npm install

# 2. Set Apollo API key (optional - can enter in UI)
export APOLLO_API_KEY="your_key_here"

# 3. Run server
node server.js

# 4. Open browser
# http://localhost:3000
```

---

## What This Does

### Problem
You have XLSX files with lead data (email, name, company, etc.) but missing enriched fields like:
- **Job Title** (from Apollo.io)
- **Company Size** (from Apollo.io)
- **Industry** (from Apollo.io)

And you're limited to **75 Apollo API calls per month**.

### Solution
**Lead Cleaner** is a web app that:

1. **Uploads** XLSX files with lead data
2. **Auto-maps** columns (handles IT/DE/EN translations)
3. **Enriches** leads via Apollo.io API (max 75/month)
4. **Scores** leads based on Job Title, Industry, Company Size
5. **Exports** enriched data back to XLSX
6. **Tracks** monthly API usage (auto-resets)

### Workflow

```
XLSX Input                Backend Processing          XLSX Export
┌──────────────┐         ┌────────────────┐          ┌──────────────┐
│ Raw leads    │────────▶│ Upload & Map   │──────────▶│ Enriched     │
│ (no enrich)  │         │ Column headers │          │ leads        │
└──────────────┘         └────────────────┘          │ (with data)  │
                                │                     └──────────────┘
                                │
                         ┌───────▼────────┐
                         │ Apollo.io API  │
                         │ (max 75 calls) │
                         └────────────────┘
```

---

## Architecture

### Three-Tier Stack

```
┌─────────────────────────────────────────┐
│         Frontend (Browser)              │
│  - HTML/CSS/Vanilla JS                  │
│  - SheetJS for XLSX parsing             │
│  - Responsive dark UI                   │
└─────────────┬───────────────────────────┘
              │ HTTP/JSON
┌─────────────▼───────────────────────────┐
│         Backend (Node.js)               │
│  - Express.js server                    │
│  - Apollo.io proxy (security)           │
│  - Monthly usage tracking (filesystem)  │
└─────────────┬───────────────────────────┘
              │ HTTPS API
┌─────────────▼───────────────────────────┐
│      Apollo.io API (External)           │
│  - /people/match endpoint               │
│  - Job Title, Industry, Company Size    │
└─────────────────────────────────────────┘
```

### File Structure

```
lead-cleaner/
├─ server.js                        # Entry point: bootstrap + shutdown handler
├─ package.json                     # Dependencies
├─ docker-compose.yml               # Dev stack: Keycloak + PostgreSQL
├─ usage.json                       # Monthly API tracking (auto-created)
├─ .env.example                     # Environment variables template
├─ src/
│  ├─ app.js                        # Express composer (importable without .listen)
│  ├─ config/env.js                 # Environment config
│  ├─ routes/
│  │  ├─ enrich.js                  # POST /api/enrich
│  │  ├─ leads.js                   # Lead management routes
│  │  └─ usage.js                   # GET /api/usage
│  ├─ services/
│  │  ├─ apollo.js                  # Apollo.io client (single API contact point)
│  │  ├─ scoring.js                 # Lead scoring logic
│  │  └─ usage-tracker.js           # Monthly quota tracking
│  ├─ middleware/
│  │  ├─ auth.js                    # Keycloak SSO auth (stub — Fase 1)
│  │  └─ security.js                # Security headers (stub — Fase 1)
│  └─ db/
│     ├─ client.js                  # PostgreSQL connection (stub — Fase 1)
│     ├─ migrations/001_init.sql    # DB schema
│     └─ repositories/
│        ├─ leads.js
│        └─ usage.js
├─ public/
│  └─ index.html                    # Full SPA (HTML + CSS + JS)
├─ docs/
│  └─ KEYCLOAK_GUIDE.md            # SSO OIDC guide (Italian)
├─ scripts/
│  ├─ migrate.js                    # DB migration runner
│  └─ keycloak-realm.json           # Keycloak realm config for local dev
├─ test/
│  ├─ test-apollo.xlsx              # Sample XLSX for testing
│  └─ prova_apollo1.json            # Sample Apollo API response
├─ README.md                        # This file
├─ BACKEND_DOCUMENTATION.md         # Detailed backend docs
└─ FRONTEND_DOCUMENTATION.md        # Detailed frontend docs
```

---

## Features

### ✅ File Upload
- Drag & drop or click to browse
- Auto-detects .xlsx and .xls formats
- Validates file structure

### ✅ Smart Column Mapping
- Recognizes Italian, German, and English column names
- Fuzzy matching for flexibility
- Handles variations (e.g., "E-Mail-Adresse" → "email")

### ✅ Data Enrichment
- Calls Apollo.io API for each lead
- Extracts: Job Title, Company Size, Industry
- 400ms delay between calls (rate limiting)
- Visual feedback during enrichment

### ✅ Lead Scoring
Automatic scoring based on:
- **Job Title**: +5 for C-level/IT roles, -15 for Student/HR
- **Industry**: +10 for target industries (Banking, IT Services, etc.)
- **Company Size**: +5 if ≥ 500 employees
- **Total range**: -15 to +25

### ✅ Visual Status
- **Green border** = Fully enriched (3/3 fields)
- **Yellow border** = Partially enriched (1-2 fields)
- **No color** = Not enriched yet

### ✅ Interactive Table
- Sort by any column (click header)
- Color-coded scores (green/yellow/red)
- Enriched fields highlighted in green text
- Responsive design

### ✅ Rate Limiting
- Tracks 75 calls per month (Apollo limit)
- Auto-resets on new month
- Shows usage in header bar
- Graceful stop when limit reached

### ✅ Export
- Exports filtered data to XLSX
- Includes all enriched fields
- Excludes internal fields (Score, etc.)
- Filename: `leads_enriched_YYYY-MM-DD.xlsx`

### ✅ Security
- API key NOT sent from browser (proxy via backend)
- Key stored in browser localStorage
- Can enter key in UI or via env var

---

## API Endpoints

### GET `/api/usage` - Check monthly usage

```bash
curl http://localhost:3000/api/usage
```

Response:
```json
{
  "month": "2026-04",
  "calls_used": 14,
  "calls_remaining": 61,
  "monthly_limit": 75
}
```

### POST `/api/enrich` - Enrich a lead

```bash
curl -X POST http://localhost:3000/api/enrich \
  -H "Content-Type: application/json" \
  -H "X-Apollo-Key: your_key" \
  -d '{
    "email": "dylan.brossel@dieteren.be",
    "first_name": "Dylan",
    "last_name": "Brossel"
  }'
```

Response (200 OK):
```json
{
  "job_title": "Sales Manager",
  "company_size": 250,
  "industry": "IT Services",
  "calls_used": 15,
  "calls_remaining": 60
}
```

Response (No match):
```json
{
  "job_title": null,
  "company_size": null,
  "industry": null,
  "calls_used": 15,
  "calls_remaining": 60
}
```

Response (Limit reached - 429):
```json
{
  "error": "Monthly Apollo API limit reached",
  "calls_used": 75,
  "monthly_limit": 75
}
```

---

## Configuration

### Environment Variables

```bash
# Optional - set Apollo API key
APOLLO_API_KEY=your_key_here

# Optional - change port (default 3000)
PORT=8080
```

### Runtime Configuration

Edit these constants in `server.js`:
```javascript
const PORT = process.env.PORT || 3000;
const APOLLO_API_KEY = process.env.APOLLO_API_KEY || '';
const MONTHLY_LIMIT = 75;  // ← Apollo limit
```

Edit these constants in `public/index.html`:
```javascript
const COLUMNS = [
  // Add/remove columns here
];

const TARGET_TITLES = new Set([
  'CEO', 'CTO', 'CIO', ...
  // Add/remove job titles for scoring
]);

const TARGET_INDUSTRIES = new Set([
  'Banking', 'IT Services', ...
  // Add/remove industries for scoring
]);
```

---

## Data Model

### Lead Object

```javascript
{
  // Original fields from XLSX
  salutation: "Mr.",
  first_name: "Dylan",
  last_name: "Brossel",
  email: "dylan.brossel@dieteren.be",
  company: "D'Ieteren Group SA",
  type: "Lead",
  contact_owner: "John Doe",
  country: "Belgium",
  legal_basis: "Consent",
  
  // Enriched from Apollo.io
  job_title: "Sales Manager",         // From Apollo
  industry: "IT Services",             // From Apollo
  company_size: "250",                 // From Apollo
  
  // Internal state
  _score: 20,                          // Computed score
  _enriched: ['job_title', 'industry', 'company_size']  // Which fields enriched
}
```

### Usage Tracking (usage.json)

```json
{
  "month": "2026-04",
  "calls": 14
}
```

Resets automatically on new month (checked on every GET /api/usage).

---

## Lead Scoring Rules

### Target Job Titles (+5 points)

C-level, IT leadership, and specific roles:
```
CEO, CTO, CIO, COO, CFO, CMO,
HEAD OF IT, IT MANAGER, IT DIRECTOR,
ENTERPRISE ARCHITECT, VP DIGITAL TRANSFORMATION,
CHIEF INFORMATION OFFICER, CHIEF TECHNOLOGY OFFICER,
... (35 total)
```

### Negative Job Titles (-15 points)

```
STUDENT, HR
```

### Target Industries (+10 points)

Financial, tech, and government sectors:
```
Banking, Financial Services, IT Services,
Insurance, Telecommunications,
Utilities, Government Administration,
Investment Banking, Media,
... (20+ total)
```

### Company Size (+5 points)

```
If company_size >= 500: +5 points
```

### Example Scores

```
CEO at Banking with 1000 employees:
  +5 (CEO) +10 (Banking) +5 (size >= 500) = +20 (GREEN)

Student at Retail with 50 employees:
  -15 (Student) + 0 (Retail not target) + 0 = -15 (RED)

Sales Rep at Restaurant with 20 employees:
  0 + 0 + 0 = 0 (NEUTRAL)
```

---

## Error Handling

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| **"API key not configured"** | No X-Apollo-Key header | Set APOLLO_API_KEY env var or enter in UI |
| **"API key invalid"** (401) | Wrong/expired key | Check Apollo.io credentials |
| **"Monthly limit reached"** (429) | All 75 calls used | Wait until next month or contact Apollo |
| **"Network error"** | Fetch failed | Check internet connection |
| **"No leads found"** | XLSX file empty or wrong format | Verify XLSX structure |
| **"Apollo non-JSON response"** | Apollo server error | Retry later |

### Debugging

**Backend logs** (terminal):
```
Lead Cleaner running at http://localhost:3000
Apollo call #1 | status 200 | email: dylan.brossel@dieteren.be
Apollo call #2 | status 401 | error: Invalid API key
```

**Frontend logs** (Browser F12 → Console):
```javascript
Apollo error: { error: "Invalid ac..." }
Enrich error: TypeError: fetch failed
```

---

## Use Cases

### Use Case 1: Monthly Lead Import (First of Month)

```
Day 1-5 April:
  1. Upload XLSX with 307 new leads
  2. Click "Enrich with Apollo"
  3. Backend makes 75 API calls
  4. 75 leads enriched, 232 left pending
  5. Export XLSX with enriched data
  6. Store pending leads aside for next month

Day 6-30 April:
  - No API calls (limit exhausted)
  - Pending leads can only be viewed/exported as-is
  - Wait until 1 May for new quota

Day 1 May:
  - API usage resets automatically
  - Can enrich the 232 pending leads from April
```

### Use Case 2: Iterative Enrichment

```
Upload → Enrich (batch 1) → Export
  ↓
Review Results → Re-upload → Enrich (batch 2)
  ↓
Final Export
```

---

## Performance & Limits

| Aspect | Limit | Reason |
|--------|-------|--------|
| File size | 10MB | Browser memory |
| Leads per file | 1000+ | UI performance |
| API calls | 75/month | Apollo plan |
| Call delay | 400ms | Rate limiting |
| Timeout | 30s | Node.js default |
| Usage tracking | Filesystem | Simple, no DB needed |

---

## Security Considerations

✅ **What's Secure:**
- API key NOT in browser console (stored server-side)
- No plaintext credentials in code
- HTTPS recommended for production
- Input validation on server side

⚠️ **What to Watch:**
- API key in localStorage (JavaScript can access)
- No auth/login system
- Single-user setup (shared server = shared quota)
- XLSX parsing is client-side (no server validation)

---

## Deployment

### Local Development

```bash
node server.js
# → http://localhost:3000
```

### Production (Example: Heroku)

```bash
# Set environment variable
heroku config:set APOLLO_API_KEY=your_key

# Deploy
git push heroku main
```

### Production (Example: Docker)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install --production
ENV APOLLO_API_KEY=${APOLLO_API_KEY}
EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Troubleshooting

### "Can't find variable: XLSX"
**Cause:** Frontend opened as `file://` instead of via server  
**Fix:** Use `http://localhost:3000` not file path

### "Port 3000 already in use"
**Cause:** Another process on port 3000  
**Fix:**
```bash
# Kill existing process
lsof -ti :3000 | xargs kill -9

# Or change port
PORT=8080 node server.js
```

### "Apollo API key not working"
**Cause:** Invalid key or expired credentials  
**Fix:** 
1. Check key in Apollo.io dashboard
2. Verify X-Api-Key header format
3. Try test request: `curl -H "X-Api-Key: YOUR_KEY" https://api.apollo.io/api/v1/people/match`

### "Enrichment stops after few leads"
**Cause:** Monthly limit reached (75 calls)  
**Fix:** Check usage bar, wait until next month, or upgrade Apollo plan

---

## Documentation Structure

| Document | Purpose | Audience |
|----------|---------|----------|
| **README.md** (this file) | Overview, setup, deployment | Everyone |
| **BACKEND_DOCUMENTATION.md** | Detailed backend architecture | Backend devs, system admins |
| **FRONTEND_DOCUMENTATION.md** | Detailed frontend logic | Frontend devs, QA |

---

## Contributing

### Adding a New Job Title to Scoring

1. Edit `FRONTEND_DOCUMENTATION.md` to understand scoring
2. Open `public/index.html`
3. Find `const TARGET_TITLES = new Set([`
4. Add your title to the array
5. Test enrichment with a sample lead

### Changing the API Limit

1. Edit `server.js`: `const MONTHLY_LIMIT = 75;`
2. Restart server
3. usage.json will reset on next call

### Adding Support for a New Language

1. Edit `ALIASES` object in `public/index.html`
2. Add language-specific column names
3. Test with sample XLSX in that language

---

## FAQ

**Q: Why do I need a backend? Can't I call Apollo directly from the browser?**  
A: CORS restrictions. Also, API key would be exposed to users. Backend proxy is more secure.

**Q: What if Apollo doesn't find a match?**  
A: All three fields return `null`. The call still counts toward your 75 limit.

**Q: Can I increase the 75-call monthly limit?**  
A: Only if Apollo upgrades your plan. Change `MONTHLY_LIMIT` in `server.js` if you pay for more.

**Q: Is there a way to manually reset usage tracking?**  
A: Yes, delete `usage.json` file (or edit it to `{"month": "2026-04", "calls": 0}`).

**Q: Can multiple users use this simultaneously?**  
A: Yes, but they share the 75-call monthly quota. Each client needs to enter the same API key.

**Q: What happens if the server crashes?**  
A: Restart it. `usage.json` will persist the call count (data is safe).

---

## License & Credits

Built with:
- **Express.js** - Web framework
- **SheetJS** - XLSX parsing
- **Apollo.io** - Data enrichment API

---

## Support

For issues:
1. Check **Troubleshooting** section above
2. Review **BACKEND_DOCUMENTATION.md** or **FRONTEND_DOCUMENTATION.md**
3. Check browser console (F12) for frontend errors
4. Check terminal for backend errors
5. Verify Apollo API key is valid

---

**Last Updated:** 2026-04-13  
**Version:** 1.0.0
