# Contract: Model Output Format (ML -> Backend API)

**Parties:** Hesham (Member 2, ML & Evaluation) <-> Member 4 (Backend)
**Status:** Draft v1.0 - Week 1
**Source of truth:** docs/success_metrics.md (Sections 4.2, 4.4)
**Change process:** any change to this file needs both signatures below.

## 1. Request (Backend -> ML)
| Field | Type | Allowed values | Required |
|---|---|---|---|
| ticket_id | string | unique id | yes |
| text | string | original ticket text | yes |
| language | string | en / ar-msa / ar-eg | yes |

## 2. Response (ML -> Backend) - the 5 guaranteed fields
| Field | Type | Allowed values | Meaning |
|---|---|---|---|
| ticket_id | string | same as request | echo |
| predicted_category | string | payment / account / technical / delivery | top class |
| confidence | float | 0.0 - 1.0 | model probability of top class |
| decision | string | auto / human_review | routing decision |
| model_version | string | e.g. baseline-v1 | traceability |

Example:
{
  "ticket_id": "T-000123",
  "predicted_category": "technical",
  "confidence": 0.64,
  "decision": "human_review",
  "model_version": "baseline-v1"
}

## 3. Decision rule (fixed in week 1)
- confidence >= 0.80 AND (top1 - top2) >= 0.10  ->  auto
- otherwise                                     ->  human_review

## 4. Backend obligations (Member 4)
1. human_review tickets must reach a human agent; the backend must NOT
   auto-reply to the customer using the predicted_category of such tickets.
2. predicted_category stays attached to human_review tickets as a
   suggestion for the agent (never hidden).
3. Backend logs model_version with every decision (audit trail).

## 5. ML obligations (Member 2)
1. Response always contains all 5 fields, even on internal fallback.
2. Threshold T=0.80 is provisional; retuning happens only with data and
   is announced in a new version of this contract first.

## Sign-of
| Role | Name | Date | Confirmed |
|---|---|---|---|
| ML & Evaluation | Hesham | 2026-10-30 | yes |
| Backend | Member 4 | | |
