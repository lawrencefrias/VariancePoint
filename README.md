# VariancePoint

VariancePoint is a technology futures intelligence platform that helps organizations measure strategic drift, forecast technology risk, and simulate alternate outcomes from present-day architecture decisions.

## Monorepo layout

- `apps/web` — Next.js + TypeScript executive and engineering UI
- `apps/api` — FastAPI service for scoring, simulation, and public APIs
- `packages/*` — reusable engines/connectors/visualization packages
- `datasets/*` — seed datasets for lifecycle, technologies, vendors, and CVEs metadata
- `docs/*` — architecture, roadmap, scoring, and governance docs

## Quick start

### API

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

### Web

```bash
cd apps/web
npm install
npm run dev
```
