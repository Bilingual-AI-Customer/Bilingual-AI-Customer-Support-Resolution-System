# Phase Plan — Weeks 2–4

**Version:** 1.0 — 2026-11-03
**Owners:** written by Hesham (Member 2); each row has one named owner.
**Rule:** every deliverable lands on `develop` via PR (`CONTRIBUTING.md`).
"Done" means merged, not just pushed to a feature branch.

## Week 2 — Foundations (Sun 1 Nov → Thu 5 Nov)

| # | Deliverable | Owner | Where it lands |
|---|---|---|---|
| 1 | Final data on `develop`: `eg_complaints_final.csv` (AR, 25,576), `train_mapped_final.csv` + `test_mapped_final.csv` (EN), approved `banking77_intents_to_categories.csv` (mapping v2, 14 flagged) | Hesham | `data/` |
| 2 | Reference docs: `problem_statement.md`, `architecture_view.md`, `plan.md`, `DATA_LICENSES.md`, `requirements.txt`, `LICENSE` — reviewed and merged | Hesham drafts · Member 4 reviews & merges | `docs/`, root |
| 3 | Contracts signed: `unified_data_schema.md` (Member 1), `model_output_contract.md` v1.1 (backend owner) | Member 1, Rawda, Member 4 | `docs/contracts/` |
| 4 | AR golden set, batch 1: 60 hand-verified rows (min 30/category by end of set), UTF-8 CSV, unified schema | Member 1 | `data/golden/ar_eg_golden_batch1.csv` |
| 5 | KB first drafts: `rag/kb/faq.md` + `rag/kb/payment-policy.md` (bilingual, per kb-plan standards) | Ziad (+ Member 1 questions) | `rag/kb/` |
| 6 | Chunking script + retrieval pilot on 15–20 known Q/A: correct chunk in top-1/top-3? results table | Ziad | `rag/`, `docs/rag_retrieval_eval.md` |
| 7 | PostgreSQL schema.sql + seed.sql (20 AR + 5 EN tickets) + users/roles + CRUD endpoints per `api-contract.md` | Rawda | `backend/`, `db/` |
| 8 | Frontend reads the real API (list, details, status, reply) instead of local demo data | Rawda | `Front/` |
| 9 | EN baseline re-run on mapping v2 (numbers before/after recorded) | Hesham | `ml/baseline/` |

**Week-2 exit checklist:** final data merged · docs merged · 2 contracts signed
· golden batch 1 delivered · KB drafts in `rag/kb/` · backend with DB + CRUD +
seed · frontend on real API · baseline v2 numbers in `results.md`.

## Week 3 — Classification live (Sun 8 Nov → Thu 12 Nov)

| # | Deliverable | Owner |
|---|---|---|
| 1 | Classification service: FastAPI `POST /classify` exactly per `ai-inference-api-contract.md` §3, URL from config, returns the 5 contract fields | Hesham |
| 2 | Arabic baseline v1 on golden batch 1 (pilot numbers, per-language report) | Hesham |
| 3 | Backend → `/classify` integration on ticket create; store `category/confidence/model_version`; gate rule applied; graceful fallback when service down | Rawda |
| 4 | Golden set batch 2 → total ≥ 120 (30/category floor) | Member 1 |
| 5 | KB: remaining documents drafted (`account-support.md`, `technical-support.md`, delivery/shipping pair) | Ziad |
| 6 | Retrieval eval extended to the new documents; chunk metadata finalized | Ziad |
| 7 | `docker-compose`: `backend` + `classify` services joined; README quickstart verified on a clean machine | Hesham + Rawda |

**Week-3 exit checklist:** a ticket created in the UI gets classified and
stored with confidence + decision, audit row written, and it works through
docker-compose alone.

## Week 4 — Resolution loop + freeze (Sun 15 Nov → Thu 19 Nov)

| # | Deliverable | Owner |
|---|---|---|
| 1 | RAG prototype: `POST /suggest-reply` per contract §4, with sources and abstention | Ziad |
| 2 | UI shows suggested reply + sources + "AI suggestion — agent decides" | Rawda |
| 3 | Evaluation report: per-language Macro F1 + per-class P/R + gate scan, updated in `docs/success_metrics.md` + `results.md` | Hesham |
| 4 | Agent-framework decision note (one page: what, why, what we defer) | Ziad + Hesham |
| 5 | `data/splits/` frozen (fixed seed, documented) — after this, no edits | Hesham |
| 6 | Week summaries + demo walkthrough script (create → classify → reply → resolve) | all |

**Standing gates (do not change without a new contract version):**
EN Macro F1 ≥ 0.80 · AR Macro F1 ≥ 0.75 · min per-class F1 ≥ 0.60 ·
T = 0.80 gate · per-language reporting only.

## Risk register (living)

| Risk | Owner | Response |
|---|---|---|
| Golden set slips past week 3 | Member 1 + Hesham | batch discipline (60/week); Hesham keeps pilot-only labels |
| Backend/ML integration mismatch | Rawda + Hesham | contract first; contract tests before UI work |
| KB docs stall on "unknown policy values" | Ziad | kb-plan rule: mark `Team confirmation required`, never invent values |
| Imbalance hides failures | Hesham | Macro F1 gates + class weights + per-class report |
