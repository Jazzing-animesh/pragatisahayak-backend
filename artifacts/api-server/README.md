# PragatiSahayak Backend

Foundation layer for the PragatiSahayak Smart India Hackathon 2026 project,
an AI business advisory platform for rural Indian entrepreneurs.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
python -m app.seed.seed_locations
python -m app.seed.seed_schemes
python -m app.seed.seed_categories
python run.py
```

The health check is available at `http://localhost:5000/api/health`.

Seed scripts are idempotent and can safely be run repeatedly.