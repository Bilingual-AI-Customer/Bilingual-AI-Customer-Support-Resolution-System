# Success Metrics Documentation

**Project:** Bilingual AI Customer Support & Resolution System
**Owner:** Hesham — Member 2 (Evaluation & ML Models)
**Status:** Draft v0.1 (Week 1) — Section 1 of 4
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

*(Sections 2-4 — Macro F1/P/R in practice, per-language evaluation,
confidence & handoff — to be added to this draft.)*