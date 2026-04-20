# Study Assistant — AAI 5015

A working implementation of the **Spaced Repetition Topic Recommender** described in the three AAI 5015 final-project papers. Study content is pulled from the course Canvas (modules 6–10: probability and statistics). The app implements all three mathematical layers end-to-end:

1. **Part 1 — Bayesian belief updating** with an exponential time-decay prior (`backend/bayes.py`)
2. **Part 2 — Linear regression** via closed-form OLS (`backend/regression.py`)
3. **Part 3 — Gradient descent**, batch + SGD (`backend/gradient.py`)

## Quickstart

```bash
cd ~/code/study-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set your Anthropic key — both seed and the backend auto-load .env
cp .env.example .env
# edit .env and paste your sk-ant-... key

python scripts/seed.py               # pulls content + generates questions via Haiku 4.5
uvicorn backend.main:app --reload --port 8765
```

Then open <http://localhost:8765>.

> You can run `seed.py` without a key — it will load topic content but skip question generation. Fill in `.env` and rerun to generate questions.

## Project layout

```
study-assistant/
├── backend/
│   ├── bayes.py         # Part 1: Bayesian posterior + exponential time decay
│   ├── regression.py    # Part 2: closed-form OLS
│   ├── gradient.py      # Part 3: batch GD and SGD
│   ├── db.py            # SQLite connection + queries
│   ├── schema.sql       # topics, questions, quiz_attempts
│   └── main.py          # FastAPI app + static file serving
├── scripts/
│   └── seed.py          # ingest topics/*.md, generate questions via Haiku 4.5
├── data/
│   ├── topics/          # 17 Canvas sections (modules 6–10) as markdown
│   └── study.db         # created on first run
└── frontend/
    └── index.html       # SPA: dashboard + Math Lab + About
```

## How the math actually runs in the app

- **Dashboard**: topics are ranked by *current* retention = last Bayesian belief decayed exponentially from the time of your last review to now. Never-reviewed topics surface first.
- **Quiz submission**: the backend rebuilds your belief `P(retains)` for that topic by replaying all attempts through `bayes.current_belief`. The current (days_since_review, score) is appended as the newest event before the posterior is computed.
- **Math Lab — Regression tab**: pulls every quiz attempt, plots (days_since_review, score·100), and overlays the closed-form OLS fit with r and R².
- **Math Lab — Gradient Descent tab**: runs either batch GD or SGD on the same data with your chosen learning rate and epoch count, then plots both the fitted line (vs. the OLS reference) and the loss curve so you can see convergence.

## Canvas source

Study topics come from AAI 5015 (Spring 2026) Canvas, modules 6–10. Each section in Canvas is one `.md` file in `data/topics/`. Rerunning `seed.py` upserts content but only generates questions for topics that don't yet have any — safe to re-run.
