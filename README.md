# AI Value Bets

A Streamlit app + scheduled emailer that finds **value bets** across 1X2, BTTS, and Over/Under markets by combining AI confidence with bookmaker odds. Includes caching, tests, and GitHub Actions automation.

---

## ✨ Features
- **Correct value math** and **edge** calculations
- **Daily cache** so you don’t resend the same picks
- **Email delivery** (Gmail App Password)
- **Streamlit UI** with sortable table
- **Pytest suite** to protect core formulas
- **CI/CD** via GitHub Actions:
  - ✅ `tests.yml` runs pytest on each push/PR
  - 📩 `daily_email.yml` runs tests, then sends the daily email (08:00 Mauritius / UTC+4)

---

## 🧮 Formulas

Let:
- `p = AI Confidence / 100`
- `o = Bookie Odds`
- `q = 1 / o` (implied probability)

**Value %**  
```
Value % = ((p * o) - 1) * 100
```
**Edge %**  
```
Edge % = (p - q) * 100
```

**Example** (72% @ 2.10):  
- `p = 0.72`, `o = 2.10`, `q = 1/2.10 ≈ 0.47619`  
- `Value % = (0.72 * 2.10 - 1) * 100 = 51.2%`  
- `Edge %  = (0.72 - 0.47619) * 100 ≈ 24.38%`

---

## 🚀 Quick Start (Local)

```bash
pip install -r requirements.txt

# Run tests
pytest -q

# Run Streamlit app
streamlit run app.py
```

Create a `.env` file (copy from `.env.example`) and set:
```
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

---

## ☁️ GitHub Actions (CI + Daily Email)

**Secrets (Repo → Settings → Secrets → Actions):**
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD` (16-char Gmail App Password, requires 2FA)

**Workflows:**
- `.github/workflows/tests.yml` → installs deps and runs pytest
- `.github/workflows/daily_email.yml` → runs tests; if green, loads `.env` from Secrets and executes `python run_email.py`

Manually trigger from **Actions** tab or wait for the daily schedule (08:00 MUT).

---

## 📁 Project Structure

```
.
├── app.py
├── cache_manager.py
├── email_sender.py
├── odds_scraper.py
├── predictions.py
├── requirements.txt
├── run_email.py
├── value_calc.py
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── daily_email.yml
└── tests/
    └── test_value_calc.py
```

---

## 🔐 Security Notes
- Do **not** commit your real `.env`. Use `.env.example` for variables only.
- Gmail SMTP requires **2FA enabled** and a **Gmail App Password**.
- GitHub Actions use **Secrets** instead of committing credentials.

---

## 🛣️ Next Steps
- Swap demo data (`predictions.py`, `odds_scraper.py`) with live sources
- Add fuzzy match for team names
- Extend markets beyond 1X2/BTTS/Over-Under
- Optional: Telegram/WhatsApp alerts
