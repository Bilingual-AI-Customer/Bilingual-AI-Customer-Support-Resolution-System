# Data Sources & Licenses

**Version:** 1.0 — 2026-11-03
**Rule:** every dataset used for training or evaluation must be listed here
with its source, license, and what we did to it. No dataset enters `data/`
without a row in this file.

## 1. English — Banking77 (PolyAI)

| Item | Value |
|---|---|
| Source | `PolyAI/banking77` on Hugging Face — https://huggingface.co/datasets/PolyAI/banking77 |
| License | **CC-BY-4.0** — attribution is **mandatory** |
| Contents | 10,003 train / 3,080 test customer messages, human-labeled into 77 banking intents |
| What we did | Mapped the 77 intents to our 4 categories with `data/banking77_intents_to_categories.csv` (45 payment / 25 account / 5 technical / 2 delivery, 14 intents flagged `needs_review`). Files: `data/banking77/train_mapped_final.csv`, `data/banking77/test_mapped_final.csv` |
| Citation (keep in any report/paper) | "Castein, D., Mrkšić, N., & Vulić, I. (2022). *How to Train your Chatbot with Dialogue Data: Lessons Learned from the Banking Domain.* Or: dataset Banking77 by PolyAI, https://github.com/PolyAI-LDN/task-specific-datasets, license CC-BY-4.0." |

> The upstream paper for Banking77: Iñigo Casanueva, Tadas Temčinas, Daniela
> Gerz, Ivan Vulić, Nikola Mrkšić — *Efficient Intent Detection with Dual
> Sentence Encoders* (2020), dataset released by PolyAI under CC-BY-4.0.

## 2. Arabic — Egyptian complaints corpus (`eg_complaints_final.csv`)

| Item | Value |
|---|---|
| Source | Public user reviews/complaints collected from the Google Play pages of Egyptian consumer apps (e.g. InstaPay, myFawry, NBE Mobile, CIB, QNB, eKhales, Masary, WEPay, VodaCash, Aman, OPay, Vodafone Cash, Halan, plus e-commerce/delivery apps), collected 2026-10/11 via `scripts/scrape_eg_apps.py` in the team workspace |
| Size | 25,576 rows; columns `complaint_text, category, priority, sentiment` |
| Labels | **Weak labels** — rule-based mapping to the 4 categories + priority + sentiment; not human annotations. Human verification happens only in the golden sets |
| License | No explicit dataset license — content is public user-generated text. **Academic/project use only; not for redistribution.** If any platform or author requests removal, we comply |
| PII | Reviewer usernames and IDs are dropped; text is kept as-is apart from that. If PII is spotted during golden-set review, the row is excluded |

## 3. Golden evaluation sets

| Set | Owner | Size | Labels |
|---|---|---|---|
| `data/golden/ar_eg_golden_*.csv` | Member 1 | min 120, target 200 (≥30/category) | Hand-verified: category (+ priority), reviewer column for disagreements |
| EN fixed test set | from Banking77 upstream | 3,080 | upstream human labels, mapped |

## 4. Code license

Repository code: MIT (see root `LICENSE`). The datasets above keep their own
terms — the MIT license covers our code and derived scripts only, not the
data files.

## 5. Red-flag rules (from CONTRIBUTING.md)

1. `data/raw/*` is never committed (repo is public).
2. No `.env`, no credentials, no customer personal data in any commit.
3. Any new dataset → add a row here **in the same PR** that adds the files.
