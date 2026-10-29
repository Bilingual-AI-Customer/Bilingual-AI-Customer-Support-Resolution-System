# Success Metrics Documentation

**Project:** Bilingual AI Customer Support & Resolution System
**Owner:** Hesham — Member 2 (Evaluation & ML Models)
**Status:** Draft v0.2 (Week 1) — Sections 1-4 complete
**Scope:** Classification (payment / account / technical / delivery) x Languages (English, MSA Arabic, Egyptian Arabic)

---

## 1. Why Accuracy Alone Is Misleading

### 1.1 Claim
With imbalanced classes, a model can achieve high accuracy while failing
completely on one or more categories. Therefore accuracy is **not acceptable
as a standalone success criterion** for this project.

### 1.2 Evidence from our own data
Mapping the 77 BANKING77 intents onto the 4 project categories (Week-1 EDA):

| Category  | Share of data | vs. delivery |
|-----------|--------------:|-------------:|
| payment   |         61.9% |          7.1x |
| account   |         19.4% |          2.2x |
| technical |         10.0% |          1.1x |
| delivery  |          8.7% |          1.0x |

The largest class outweighs the smallest by ~7x — exactly the setting
where accuracy misleads.

### 1.3 Thought experiment: the dummy model
Take 100 tickets: 90 payment + 10 delivery (simplified mirror of the
imbalance above). Model: predicts **"payment"** for every ticket without
reading anything.

| Metric | Value | Reading |
|---|---:|---|
| Accuracy | 90% | Looks excellent on a dashboard |
| Recall (payment) | 100% | Majority class fully covered |
| Recall (delivery) | **0%** | Not a single delivery ticket caught |
| Macro recall | 50% | Exposes the failure accuracy hides |

With our real 4-category distribution, the same dummy model scores 61.9%
accuracy while its recall on account, technical and delivery is 0%.

### 1.4 Why this matters for customer support
1. **Rare categories are the expensive ones.** Delivery complaints and
   technical failures come from already-frustrated customers; missing them
   costs more than misrouting a payment question.
2. **Accuracy hides per-category failure.** A "90% accurate" routing model
   that sends every delivery complaint to the wrong team is a failed
   product with a beautiful number.
3. **Errors are not equal.** Accuracy weights every mistake the same;
   in support operations they are not.
4. **A single number blocks per-language diagnosis.** Overall accuracy can
   look acceptable while the Arabic side is quietly collapsing (Section 3).

### 1.5 Decision
- Accuracy is **reported for reference only**, labeled non-decisional.
- **Macro F1 is the primary metric** (Section 2), with per-class
  Precision and Recall.
- Every metric is computed **per language separately** (Section 3).
- Confidence threshold and human-handoff rule are defined in Section 4.

## 2. The Metrics We Use — Precision, Recall, F1 in Plain Language

### 2.1 Judging ONE category
For any category (say **delivery**), each prediction is one of:
- **TP** — real delivery ticket, model routed it correctly
- **FP** — not delivery, but model routed it there (false alarm, wasted agent time)
- **FN** — real delivery ticket the model missed (ignored customer)

| Metric | Formula | Question it answers | Who it protects |
|---|---|---|---|
| Precision | TP / (TP+FP) | Of tickets routed to delivery, how many were truly delivery? | The team (noise) |
| Recall | TP / (TP+FN) | Of all real delivery tickets, how many did we catch? | The customer (silence) |
| F1 | harmonic mean of P & R | One balanced number per category | Both (punishes one-sided models) |

### 2.2 Worked examples (100 tickets, 20 real delivery)
**Scenario A — healthy model:** flags 15 tickets, 12 correct.
Precision = 12/15 = **80%**, Recall = 12/20 = **60%**, F1 = **68.6%**.

**Scenario B — the precision trap:** flags only 5, all 5 correct.
Precision = 5/5 = **100%**, Recall = 5/20 = **25%**, F1 = **40%**.
A "100% precise" model that abandons 15 of 20 delivery complaints is NOT a success.

**Scenario C — the recall trap:** flags 35, catches all 20 real (+15 false alarms).
Precision = 20/35 = **57%**, Recall = **100%**, F1 = **72.7%**.
Catches everything but floods the team with noise.

**Lesson: Precision and Recall are trade-offs; F1 exposes one-sided models
that either metric alone would flatter.**

### 2.3 Why MACRO F1 is our primary metric
In single-label multiclass, Micro-F1 equals accuracy. Re-run the Section-1
dummy model (90 payment + 10 delivery, always predicts "payment"):

| Aggregation | Value |
|---|---:|
| Micro F1 (= accuracy) | 90% |
| Macro F1 (mean of per-class F1: payment 94.7%, delivery 0%) | **47.4%** |

The ~43-point gap between micro and macro IS the hidden failure, now visible.

- **Macro F1** → every category counts equally → **PRIMARY metric**.
- Weighted F1 → dominated by majority classes → same hiding problem as
  accuracy → rejected.
- Accuracy / Micro F1 → reported for reference only (see Section 1).

### 2.4 Verification
`ml/evaluation/metrics_101.py` reproduces scenarios A-D in pure Python.

## 3. Per-Language Evaluation — No Pooled Numbers for Decisions

### 3.1 Why pooling languages hides the problem
Arabic and English differ in morphology, tokenization and dialects
(MSA vs Egyptian Arabic). A model can be excellent on English and
collapse on Arabic while the pooled metric still looks "acceptable".

Worked example (20 tickets, 2 categories):

| Bucket | payment P/R/F1 | delivery P/R/F1 | Macro F1 |
|---|---|---|---:|
| English | 83% / 100% / 90.9% | 100% / 80% / 88.9% | **89.9%** |
| Arabic  | 43% / 60% / 50.0%  | 33% / 20% / 25.0%  | **37.5%** |
| Pooled  | 62% / 80% / 69.6%  | 71% / 50% / 58.8%  | 64.2% |

Pooled says 64.2% ("needs work"). The split says: English is healthy,
Arabic has collapsed — an actionable finding, not a vague one.

### 3.2 Rules for this project
1. Every metric (Macro F1, per-class Precision/Recall) is computed
   separately per language bucket: `en`, `ar-msa`, `ar-eg`.
2. The decision number per language is Macro F1; per-class P/R are
   reported next to it.
3. Minimum support: a language x category cell with fewer than 30 test
   samples is labeled "pilot" and excluded from final decisions.
4. The `language` field in the unified schema (ticket_id, text, language,
   category, priority, status) must be validated by a sampling audit —
   wrong language tags poison every per-language metric.
5. Arabic has two varieties (MSA + Egyptian). They are evaluated as
   separate buckets; a pooled "Arabic" number may be reported but never
   used alone for decisions.

### 3.3 Dependency note
`ar-msa` test data: ArBanking77 (same 77 intents). `ar-eg` test data:
hand-labeled Egyptian reviews — owned by Member 1. Until it lands,
Arabic numbers are pilot-only.

## 4. Confidence & Human Handoff

### 4.1 Why raw predictions are not enough
The classifier outputs a probability per category. A prediction at 51%
confidence is a guess, and routing a customer ticket on a guess
misroutes it. Every model output therefore carries a **confidence**
and a **decision**.

### 4.2 The mechanism
- confidence = highest category probability of the model
- confidence >= T  ->  auto-route
- confidence <  T  ->  human_review (top guess attached as suggestion)

### 4.3 Choosing T with data, not vibes
Bucket a validation run by confidence and measure accuracy per bucket
(simulated numbers for illustration):

| Confidence bin | Tickets | Accuracy |
|---|---:|---:|
| 0.90 - 1.00 | 100 | 95.0% |
| 0.80 - 0.90 |  80 | 87.5% |
| 0.70 - 0.80 |  60 | 70.0% |
| 0.50 - 0.70 | 100 | 50.0% |

Threshold scan (rule: smallest T with >= 90% accuracy on routed):

| T | Coverage (auto-routed) | Accuracy on routed |
|---:|---:|---:|
| 0.50 | 100% | 75.6% |
| 0.60 | 70.6% | 86.3% |
| 0.70 | 70.6% | 86.3% |
| 0.80 | **52.9%** | **91.7%** |
| 0.90 | 29.4% | 95.0% |

**Decision: T = 0.80 (provisional)** — about 53% of tickets answered
automatically at 91.7% accuracy; everything riskier reaches a human.

### 4.4 Project rules
1. Model output fields (basis of the API contract with Member 4):
   predicted_category, confidence, decision (auto | human_review).
2. T = 0.80 provisional, re-tuned on real validation data, per language
   (Arabic likely needs a higher T — see Section 3).
3. Ambiguity guard: if top-1 and top-2 probabilities differ by < 0.10,
   force human_review regardless of T.
4. human_review tickets always keep the model suggestion attached.

### 4.5 Metrics reporting summary
| Metric | Role |
|---|---|
| Macro F1 per language | PRIMARY decision metric |
| Per-class Precision / Recall | Diagnosis, next to Macro F1 |
| Coverage & accuracy at T | Automation quality |
| Accuracy / Micro F1 | Reference only |