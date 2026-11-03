# Data Sources & Licenses

**Version:** 1.1 — 2026-11-03
**Change log v1.1:** fixed the Banking77 citation; clarified the Arabic corpus
usage terms (academic/non-commercial, removal on request); added the derived
Egyptian training file and the rule-based filter disclosure.
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
| Citation (keep in any report/paper) | Iñigo Casanueva, Tadas Temčinas, Daniela Gerz, Ivan Vulić, Nikola Mrkšić — *Efficient Intent Detection with Dual Sentence Encoders* (2020), dataset **Banking77** released by PolyAI, https://github.com/PolyAI-LDN/task-specific-datasets, license CC-BY-4.0 |

> The upstream paper for Banking77: Iñigo Casanueva, Tadas Temčinas, Daniela
> Gerz, Ivan Vulić, Nikola Mrkšić — *Efficient Intent Detection with Dual
> Sentence Encoders* (2020), dataset released by PolyAI under CC-BY-4.0.

## 2. Arabic — Egyptian complaints corpus (`eg_complaints_final.csv`)

| Item | Value |
|---|---|
| Source | Public user reviews/complaints collected from the Google Play pages of Egyptian consumer apps (e.g. InstaPay, myFawry, NBE Mobile, CIB, QNB, eKhales, Masary, WEPay, VodaCash, Aman, OPay, Vodafone Cash, Halan, plus e-commerce/delivery apps), collected 2026-10/11 via `scripts/scrape_eg_apps.py` in the team workspace |
| Size | 25,576 rows; columns `complaint_text, category, priority, sentiment` |
| Labels | **Weak labels** — rule-based mapping to the 4 categories + priority + sentiment; not human annotations. Human verification happens only in the golden sets |
| License | No explicit dataset license — content is public user-generated text. **Academic/project use only; non-commercial; not for redistribution.** The file is hosted in this (public) repo for coursework reproducibility; if any platform or author requests removal, we comply and remove it including from git history |
| PII | Reviewer usernames and IDs are dropped; emails/URLs/long numbers inside text are excluded at filter time; if PII is spotted during golden-set review, the row is excluded |

### 2.1 Derived training file — `eg_complaints_egy_train.csv` (v1, 2026-11-03)

| Item | Value |
|---|---|
| Built from | `eg_complaints_final.csv` (25,576) via `data/egyptian_reviews/build_egyptian_train.py` |
| Result | **18,399 rows** — technical 11,476 / payment 3,776 / account 1,785 / delivery 1,362 |
| Rule-based dialect filter | requires ≥1 strong Egyptian marker; excludes Maghrebi/Gulf/Levantine markers, texts <15 chars, PII (email/URL/7+ digit runs) |
| Label-evidence check | a row keeps its label only with strong evidence (≥1 strong keyword) or ≥2 weak ones; single strong conflicting category → reassigned (1,175 rows, 6.4%, marked `label_source=reassigned`); otherwise excluded with reason |
| Excluded rows | 7,177 — full audit trail in `data/egyptian_reviews/eg_excluded_label_check.csv` (reason per row) |
| Disclosure | the filter is **rule-based, not human annotation**; the keyword lists live in the script and are reproducible end-to-end. Official evaluation happens on the hand-verified golden sets, not on this file |

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
