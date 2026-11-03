# Bilingual AI Customer Support & Resolution System

نظام دعم عملاء ثنائي اللغة (عربي / إنجليزي): يصنّف الشكوى، يحدد أولويتها، يسترجع السياسة المناسبة، ويجهز رد مقترح بمصادره. الموظف هو صاحب القرار النهائي.

## Structure

| Folder | Content | Track |
|---|---|---|
| `data/` | raw / processed / splits (الـ splits ثابتة بعد الأسبوع 3) | Data |
| `ml/` | preprocessing, baseline, models, evaluation | Data, ML |
| `rag/` | knowledge base (`kb/`), chunking, retrieval, agent | RAG |
| `backend/` | FastAPI + database + tests | Backend |
| `Front/` | web dashboard (HTML/CSS/JS), deployed to GitHub Pages | Frontend |
| `docs/` | problem definition, architecture, API contracts, reports | All |

## Documentation

| Doc | What it is |
|---|---|
| `docs/problem_statement.md` | The problem, scope, data, success gates |
| `docs/plan.md` | Week-by-week deliverables and owners (weeks 2–4) |
| `docs/architecture_view.md` | Components, flows, data model, deployment |
| `docs/success_metrics.md` | Why Macro F1, per-language rules, gate T=0.80 |
| `docs/kb-plan.md` | Knowledge base documents and quality standards |
| `docs/DATA_LICENSES.md` | Sources, licenses, weak-label disclosure |
| `docs/contracts/` | The team contracts (data schema, model output, APIs) |

## Requirements

- Python 3.10+, Docker + Docker Compose
- `pip install -r requirements.txt`

## Quickstart

```bash
# 1. database
docker compose up -d db

# 2. backend
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload      # API docs: http://localhost:8000/docs

# 3. frontend — open Front/index.html with Live Server
#    (or the GitHub Pages URL once merged to main)
```

## Data & Licenses

Datasets and their licenses are documented in
[`docs/DATA_LICENSES.md`](docs/DATA_LICENSES.md). Short version: English data
is Banking77 (PolyAI, CC-BY-4.0 — attribution required); Arabic data is a
collected corpus with weak labels, academic use only. Training data files are
committed under `data/` (never under `data/raw/`).

## Status

- [x] Week 1: Problem + Data + Skeleton — metrics doc v0.3, 4 evaluation
      scripts, banking77 + mapping, EN baseline (Macro F1 0.9375), EDA,
      contracts drafted, kb-plan
- [ ] Week 2: Foundations — final data on develop, reference docs, contracts
      signed, AR golden set batch 1, KB first drafts + retrieval pilot,
      backend tables + CRUD + seed, frontend on real API
- [ ] Week 3: Classification live — POST /classify service, backend
      integration, golden set ≥ 120, docker-compose full stack
- [ ] Week 4: Resolution loop — POST /suggest-reply prototype, evaluation
      report, splits frozen

## Team workflow

Branches: `main` (protected) ← `develop` ← `feature/<track>-<desc>`
Commits: `type(scope): message`, where type is one of feat, fix, data, ml, docs, test, chore.
