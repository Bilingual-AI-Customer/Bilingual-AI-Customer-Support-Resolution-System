# Problem Statement

**Project:** Bilingual AI Customer Support & Resolution System
**Version:** 1.0 — 2026-11-03
**Owners:** the whole team; maintained by Hesham (Member 2, Evaluation & ML)
**Status:** Reference document — every track builds against the definitions here.
**Related docs:** `docs/success_metrics.md` (gates detail) · `docs/contracts/` (interfaces) · `docs/kb-plan.md` (knowledge base) · `docs/plan.md` (phase plan)

> **الخلاصة بالعربي:** بناء نظام يساعد فريق دعم العملاء في بنك رقمي على فرز الشكاوى الواردة بالعربي والإنجليزي تلقائيًا: تصنيف لأربع فئات، ودرجة ثقة، وقرار توجيه (آلي / مراجعة بشرية)، وبعدها اقتراح رد موثق من قاعدة معرفة. الموظف يظل صاحب القرار النهائي.

## 1. Background

The support inbox of a digital bank receives customer complaints in two
languages — Arabic (MSA and Egyptian Arabic) and English — across four
recurring domains: payments, account access, technical issues, and delivery.
Today every ticket is read and routed by hand. That creates three concrete
costs:

1. **First-response time.** Manual triage delays the first reply, and delay
   is the top driver of complaint escalation.
2. **Inconsistent routing.** Different employees route similar tickets to
   different teams, so per-team queues are noisy and reassignments repeat.
3. **Bilingual staffing.** Every shift needs people comfortable in both
   languages, even for routine questions that repeat daily.

## 2. The problem we solve

We build a **decision-support system**, not an auto-pilot: a pipeline that
reads each incoming ticket and produces

- a **category** from a fixed vocabulary: `payment / account / technical / delivery`,
- a **confidence** score and a **routing decision** (`auto` vs `human_review`),
- a **priority hint** (`low / medium / high`),
- and (later phase) a **suggested reply grounded in an approved knowledge
  base**, with sources and an explicit abstention path.

A human employee always sees the suggestion and stays the decision maker.
The system never sends anything to the customer by itself.

## 3. Scope

**In scope**
- Bilingual classification (English, MSA Arabic, Egyptian Arabic) into the 4
  categories above, with per-language evaluation.
- Priority suggestion and confidence-based handoff rule.
- Ticket backend: PostgreSQL storage, basic roles (agent / supervisor), REST
  API, audit log.
- Web dashboard (existing HTML/CSS/JS in `Front/`) reading from the real API.
- Knowledge base + retrieval (RAG) producing suggested replies with sources,
  or an explicit abstention.
- A reproducible evaluation harness (per-language metrics, confidence-gate
  scan, golden test sets).

**Out of scope**
- Sending any message to the customer automatically.
- Voice/IVR channels; integration with core banking systems.
- Fraud detection or compliance decisions.
- Training on customer personal data (datasets contain no PII by design —
  see `docs/DATA_LICENSES.md`).

## 4. Data

Two datasets, one per language, mapped to the same 4-category vocabulary
(`docs/contracts/unified_data_schema.md`):

| Source | Language | Size | Split | Notes |
|---|---|---:|---|---|
| `eg_complaints_final.csv` | Arabic (EG) | 25,576 | train only (golden eval set is hand-labeled separately) | Weak labels (rules), collected from Egyptian apps' user reviews |
| `Banking77` (PolyAI) | English | 10,003 train / 3,080 test | fixed test set | Human-labeled intents, mapped 77 → 4 |

**Category distribution (final mapping v2):**

| Category | Arabic | share | English (train) | share |
|---|---:|---:|---:|---:|
| payment | 6,718 | 26.3% | 6,512 | 65.1% |
| account | 3,272 | 12.8% | 2,890 | 28.9% |
| technical | 12,720 | 49.7% | 336 | 3.4% |
| delivery | 2,866 | 11.2% | 265 | 2.6% |

**Disclosed limitations (accepted and documented):**
1. **Imbalance.** Largest class is 4.4× the smallest in Arabic and ~25× in
   English — this is exactly why Macro F1, not accuracy, is our decision
   metric (`docs/success_metrics.md` §1–2).
2. **Weak labels.** `category` in the Arabic set and `priority/sentiment` in
   both languages are rule-based labels, not human annotations. A
   human-verified Arabic golden set (min 120 rows, target 200; ≥30 per
   category) is being built by Member 1 for all decision numbers.
3. **Delivery semantics differ by language.** English `delivery` intent
   examples are mostly about receiving a bank *card*; Arabic `delivery`
   complaints are about *products/parcels*. Both map to the same category
   label on purpose; the gap is documented and covered by the golden set.
4. **English tone.** Banking77 questions are polite requests, so weak-labeled
   priority/sentiment on the English side is almost all `neutral/low`. These
   columns are informational there, not decisional.

## 5. Success criteria (gates)

Full reasoning in `docs/success_metrics.md`. Summary:

| # | Gate | Threshold |
|---|---|---|
| G1 | English Macro F1 on fixed test (n=3,080) | ≥ 0.80 |
| G2 | Arabic Macro F1 on the hand-labeled golden set | ≥ 0.75 |
| G3 | Minimum per-class F1, any category, any language | ≥ 0.60 |
| G4 | Confidence gate T = 0.80 | coverage and routed-accuracy reported per language; `human_review` must be honored end-to-end |
| G5 | Reporting rule | every decision metric computed per language (`en`, `ar-msa`, `ar-eg`); accuracy reported as reference only |

**Current baseline (English, TF-IDF + Logistic Regression, mapping v1):**
Macro F1 = 0.9375, routed accuracy at T=0.80 = 99.5% with 65.0% coverage
(`ml/baseline/results.md`). The final mapping v2
(`data/banking77_intents_to_categories.csv`, 77 intents → 45/25/5/2 with 14
flagged for review) is now the approved one; the baseline will be re-run and
re-reported on it before the week-3 freeze.

## 6. System overview

```
Customer message
      │
      ▼
Front/ (HTML dashboard)  ──►  backend/ (FastAPI + PostgreSQL)
                                     │
                                     ├──► ml: POST /classify      (category, priority, confidence, decision)
                                     └──► rag: POST /suggest-reply (reply, sources, confidence, abstained)
                                                    │
                                                    ▼
                                             rag/kb/ approved documents
```

Interfaces are contracts, not handshakes:
- `docs/contracts/unified_data_schema.md` — the 6 data columns everyone uses.
- `docs/contracts/model_output_contract.md` — ML ↔ backend output (5 fields,
  decision rule, T = 0.80).
- `docs/contracts/ai-inference-api-contract.md` — `POST /classify` and
  `POST /suggest-reply` request/response shapes.
- `docs/contracts/api-contract.md` — the CRUD API the frontend consumes.
- `docs/kb-plan.md` — what the knowledge base contains and its quality rules.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Majority-class collapse into "looks fine" numbers | Macro F1 as primary metric + class weights + per-class report |
| Arabic dialect shift (MSA vs Egyptian) | Separate language buckets; ar-eg golden set is the decision set |
| Weak labels in training data | Human-verified golden set (min 120) gates all final numbers |
| Delivery semantics gap between languages | Documented; golden set includes both readings; per-class F1 floor G3 |
| Over-trusting the model | Hard rule: `human_review` tickets are never auto-answered (contract §4) |

## 8. Deliverables

Phase-by-phase deliverables with owners live in `docs/plan.md`. Every
deliverable lands on `develop` through a PR per `CONTRIBUTING.md`.
