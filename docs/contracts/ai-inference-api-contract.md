# AI Inference API Contract

**Status:** Proposed — not implemented in the current backend.
**Base URL:** `http://localhost:8000`
**Audience:** backend, ML/RAG, and frontend contributors.

## 1. Compatibility note

`backend/main.py` currently implements only `GET /health` and
`GET /complaints`. The frontend currently fetches only `GET /complaints`; its
new-complaint, reply, and status actions are local demo behavior. Therefore
neither endpoint in this document is currently called or implemented.

The classification category vocabulary below is deliberately aligned with
`docs/contracts/model_output_contract.md`: `payment`, `account`, `technical`,
and `delivery`. These canonical values are not the frontend display labels
(for example, `Shipping & Delivery` and `Payments & Billing`). A future
frontend integration must map canonical API values to approved display labels
or update the UI vocabulary centrally; it must not invent another category
set. The `sources` response type is a list of strings to remain compatible
with the current frontend's `sources` field.

All request and response bodies use UTF-8 JSON with
`Content-Type: application/json`. Validation failures use FastAPI's standard
`422 Unprocessable Entity` shape unless the implementation documents a
versioned alternative.

## 2. Shared definitions

| Name | Type | Accepted values / rule |
|---|---|---|
| `category` | string | `payment`, `account`, `technical`, or `delivery` |
| `priority` | string | `low`, `medium`, or `high` |
| `language` | string | `en`, `ar-msa`, or `ar-eg` |
| `confidence` | number | Inclusive range `0.0`–`1.0` |
| `ticket_id` | string | Optional caller correlation identifier, 1–128 non-whitespace characters |
| `text` | string | Customer message, 1–5,000 characters after trimming |

`language` identifies the language of `text`. When omitted in a request, the
service may detect it; on success, it must return the resolved accepted value.
The service must not claim a language outside the shared vocabulary.

## 3. `POST /classify`

**Status:** Proposed.
**Purpose:** Classify a customer message for routing. This endpoint does not
create a complaint or persist a workflow state.

### Request

| Field | Type | Required | Validation |
|---|---|---:|---|
| `text` | string | Yes | 1–5,000 non-whitespace characters |
| `language` | string | No | If supplied, one of the shared language values |
| `ticket_id` | string | No | 1–128 non-whitespace characters |

```json
{
  "ticket_id": "CS-1042",
  "text": "My card was charged twice for the same order.",
  "language": "en"
}
```

### Success response — `200 OK`

All four fields below are required.

| Field | Type | Required | Description |
|---|---|---:|---|
| `category` | string | Yes | Best canonical routing category |
| `priority` | string | Yes | Suggested operational priority; a human or workflow remains responsible for final handling |
| `confidence` | number | Yes | Confidence in the classification, from 0 to 1 inclusive |
| `language` | string | Yes | Resolved language of the submitted text |

```json
{
  "category": "payment",
  "priority": "high",
  "confidence": 0.96,
  "language": "en"
}
```

The existing ML-to-backend contract requires human review when its model
confidence is below `0.80`. A future implementation should apply that routing
decision internally or expose it through a separately approved contract; it
must not automatically send a customer reply solely from this response.

### Error examples

`422 Unprocessable Entity` — blank `text`:

```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "text must contain at least one non-whitespace character",
      "type": "value_error"
    }
  ]
}
```

`422 Unprocessable Entity` — unsupported language:

```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "language must be one of: en, ar-msa, ar-eg",
      "type": "value_error"
    }
  ]
}
```

`500 Internal Server Error` — unexpected server failure:

```json
{
  "detail": "Internal server error"
}
```

## 4. `POST /suggest-reply`

**Status:** Proposed.
**Purpose:** Produce a customer-safe draft reply using approved RAG knowledge.
The output is a suggestion for review and is not a send-message operation.

### Request

| Field | Type | Required | Validation |
|---|---|---:|---|
| `text` | string | Yes | 1–5,000 non-whitespace characters |
| `category` | string | No | One of the shared category values when known from classification |
| `language` | string | No | One of the shared language values when supplied; otherwise resolve/detect it |
| `ticket_id` | string | No | 1–128 non-whitespace characters |

```json
{
  "ticket_id": "CS-1042",
  "text": "My order has not arrived. How can I track it?",
  "category": "delivery",
  "language": "en"
}
```

### Success response — `200 OK`

All four fields below are required, including when the system abstains.

| Field | Type | Required | Validation / meaning |
|---|---|---:|---|
| `reply` | string | Yes | Draft in the resolved customer language. If `abstained` is `true`, this contains a brief, safe handoff message and no unsupported policy claim. |
| `sources` | array of strings | Yes | Zero or more approved source filenames, such as `order-tracking-guide.md`. Each source must be traceable to an approved KB document. |
| `confidence` | number | Yes | Inclusive range `0.0`–`1.0`; confidence in the grounded reply/retrieval result. |
| `abstained` | boolean | Yes | `true` when the service cannot safely give a grounded answer and human handling is needed. |

Grounded reply example:

```json
{
  "reply": "You can check your order status using the tracking steps in your account. If tracking is unavailable or the status does not resolve your issue, a support agent can help review the delivery.",
  "sources": ["order-tracking-guide.md"],
  "confidence": 0.84,
  "abstained": false
}
```

Abstention example:

```json
{
  "reply": "Your request needs review by a support agent so we can help safely.",
  "sources": [],
  "confidence": 0.0,
  "abstained": true
}
```

### Reply safety and source rules

- Use only approved, applicable KB content. Do not fabricate policy values,
  delivery times, fees, eligibility, or outcomes.
- Set `abstained` to `true` when no applicable source is retrieved, source
  scope is unclear, a requested entitlement is not documented, or the request
  requires account/payment/security verification.
- When `abstained` is `true`, `sources` may be empty and `reply` must be a
  neutral handoff rather than a policy answer.
- Do not expose internal source paths, embeddings, credentials, personal data,
  or confidential operational rules.

### Error examples

`422 Unprocessable Entity` — invalid category:

```json
{
  "detail": [
    {
      "loc": ["body", "category"],
      "msg": "category must be one of: payment, account, technical, delivery",
      "type": "value_error"
    }
  ]
}
```

`422 Unprocessable Entity` — missing required `text`:

```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "missing"
    }
  ]
}
```

`503 Service Unavailable` — retrieval dependency unavailable:

```json
{
  "detail": "Reply suggestion is temporarily unavailable"
}
```

## 5. Implementation and integration requirements

1. Add these routes only after request/response schemas, model/RAG integration,
   authentication/authorization, logging, and error handling are implemented.
2. Preserve the existing `GET /complaints` response shape until a separately
   versioned frontend migration maps its display labels and priority casing.
3. A future frontend should call `/classify` before `/suggest-reply` when a
   routing category is available, display the returned `sources` as strings,
   and clearly label the reply as an AI suggestion pending agent review.
4. Use the KB document filenames defined in `docs/kb-plan.md` as source IDs;
   do not return an untraceable display-only source name.
5. Contract changes require review by backend, ML/RAG, and frontend owners.
