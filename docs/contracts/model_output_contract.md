# Contract: Model Output Format (ML -> Backend API)

**Parties:** Hesham (Member 2, ML & Evaluation) <-> Rawda (Backend)
**Status:** Draft v1.2 - Week 2 (backend ownership moved to Rawda; decision rule unchanged from v1.1)
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
- confidence >= 0.80  ->  auto
- otherwise           ->  human_review

Note (v1.1): v1.0 also required (top1 - top2) >= 0.10. That condition is
automatically satisfied whenever confidence >= 0.55 (since top2 <= 1 - top1),
so at T = 0.80 both rules are identical - verified on the baseline:
coverage 65.0% either way. If T is ever lowered below ~0.55, the margin
condition should be re-evaluated in a new version of this contract.

Note (v1.2): backend implementation ownership moved to Rawda
(week 2). Sections 1-5 and the decision rule are unchanged from v1.1.

## 4. Backend obligations (Rawda)
1. human_review tickets must reach a human agent; the backend must NOT
   auto-reply to the customer using the predicted_category of such tickets.
2. predicted_category stays attached to human_review tickets as a
   suggestion for the agent (never hidden).
3. Backend logs model_version with every decision (audit trail).

## 5. ML obligations (Member 2)
1. Response always contains all 5 fields, even on internal fallback.
2. Threshold T=0.80 is provisional; retuning happens only with data and
   is announced in a new version of this contract first.

## Sign-off
| Role | Name | Date | Confirmed |
|---|---|---|---|
| ML & Evaluation | Hesham | 2026-10-30 | yes |
| Backend | Rawda | | |
