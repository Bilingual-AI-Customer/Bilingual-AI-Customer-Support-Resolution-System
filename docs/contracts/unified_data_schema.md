# Contract: Unified Data Schema (Data -> ML/Evaluation)

**Parties:** Hesham (Member 2, Evaluation) <-> Member 1 (Data)
**Status:** Draft v1.0 - Week 1
**Source of truth:** docs/success_metrics.md (Sections 1.2, 3.2, 3.3)
**Change process:** any change needs both signatures below.

## 1. The 6 columns (exact names, lowercase)
| Column | Type | Allowed values | Notes |
|---|---|---|---|
| ticket_id | string | unique, stable | never reused |
| text | string | non-empty | raw text, no pre-cleaning |
| language | string | en / ar-msa / ar-eg | exact codes, no variants |
| category | string | payment / account / technical / delivery | lowercase |
| priority | string | low / medium / high / empty | empty allowed in static datasets |
| status | string | open / routed / human_review / resolved / empty | empty allowed in static datasets |

## 2. File format
- UTF-8 CSV, comma-separated, header row exactly the column names above.
- One ticket per row, no merged or pivoted layouts.
- File location: data/<source>/<split>.csv (e.g. data/egyptian_reviews/train.csv)

## 3. Quality rules
1. language tags are validated by a 5% sampling audit reviewed by a
   second person - wrong tags poison every per-language metric.
2. Minimum support: 30 samples per language x category cell for decision
   numbers; below that the cell is reported as "pilot".
3. ar-eg deliverable (Member 1): hand-labeled Egyptian sample,
   minimum 120 rows (30 per category), target 200.
4. Reuse the existing data/mapping_77_to_4.csv (77 intents -> 4
   categories) for any new English source before inventing a new mapping.

## 4. Delivery checkpoint
- Every delivered file comes with a one-line count of rows per
  language x category, so evaluation verifies support before use.

## Sign-off
| Role | Name | Date | Confirmed |
|---|---|---|---|
| Evaluation & ML | Hesham | 2026-10-30 | yes |
| Data | Member 1 | | |