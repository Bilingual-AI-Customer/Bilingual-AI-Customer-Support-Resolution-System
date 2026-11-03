# Knowledge Base Plan

## 1. Purpose and scope

This plan defines the first customer-support knowledge base (KB) for the
Bilingual AI Customer Support & Resolution System. It is a content and
governance plan, not a statement of company policy. No policy values, such as
refund periods, eligibility rules, delivery fees, shipping windows, or support
hours, are approved by this document. Those values must be supplied and
approved by the business owner before publication.

The repository currently reserves `rag/kb/` for KB material and contains no
ingestion or retrieval implementation. The filenames below therefore use
lowercase kebab-case Markdown (`.md`) and are proposed for that directory. A
future ingestion pipeline must preserve the filename and the heading path as
retrieval metadata.

## 2. Content standards for every KB document

- Maintain equivalent Arabic and English content in one Markdown file. Use
  clear `## English` and `## العربية` sections, with matching heading order.
- Write Arabic in Modern Standard Arabic unless an approved customer-facing
  Egyptian Arabic variant is explicitly required. Do not machine-translate
  policy content without bilingual review.
- Give each document a version, effective date, owner, reviewer, and source
  URL or source-system reference. Do not publish a document that lacks these
  fields.
- Identify unknown business decisions with `Team confirmation required`; do
  not replace them with assumptions or placeholders presented as policy.
- Keep answers atomic and citeable: one rule, condition, or procedure per
  short section. Include product, region, channel, and effective-date scope
  where applicable.
- Avoid customer personal data, payment-card data, internal credentials, and
  employee-only operational instructions.

## 3. Planned document catalogue

### 3.1 FAQ

- **Proposed filename:** `faq.md`
- **Purpose:** Provide concise answers to recurring, low-risk customer
  questions and route customers to the more authoritative policy document when
  an answer depends on a policy.
- **Main sections:** purpose and scope; account; orders; payments; refunds;
  shipping and tracking; technical help; escalation and contact options.
- **Required information:** approved questions, approved short answers,
  related-document links, supported channels, and escalation trigger for each
  question.
- **Expected content:** question-and-answer entries only. Each entry should
  link to a policy or guide rather than duplicate detailed terms.
- **Arabic and English:** every question and answer must have an equivalent
  Arabic and English version; product names, navigation labels, and links must
  be verified in both languages.
- **Source and ownership:** support operations owns the question list;
  relevant policy owners approve answers; customer support owns periodic review.
- **RAG integration:** ingest each Q&A as a separate chunk; store
  `document=faq.md`, language, section heading, version, effective date, and
  linked policy filename. Prefer the linked policy when it conflicts with FAQ
  wording.

### 3.2 Payment Policy

- **Proposed filename:** `payment-policy.md`
- **Purpose:** Define approved guidance for payment methods and payment issues.
- **Main sections:** scope; accepted payment methods; authorization and
  charging; failed or duplicate payments; receipts and invoices; payment
  security; escalation.
- **Required information:** markets and channels covered, allowed payment
  methods, payment-status definitions, duplicate-charge investigation process,
  receipt availability, security boundaries, and escalation owner. Team
  confirmation is required for methods, currencies, fees, and processing
  timelines.
- **Expected content:** factual, customer-safe troubleshooting steps and clear
  handoff cases. It must not expose processor credentials, fraud rules, or
  payment-card handling details.
- **Arabic and English:** equivalent terminology for payment states and user
  actions; retain official payment-method names unchanged where needed.
- **Source and ownership:** finance/payments product owner is accountable;
  payment operations, legal/compliance, and support approve relevant sections.
- **RAG integration:** tag with `category=payment`; chunk by issue type; attach
  market, payment method, effective date, and version metadata. Retrieval must
  abstain or hand off when market or payment method is absent.

### 3.3 Refund Policy

- **Proposed filename:** `refund-policy.md`
- **Purpose:** State eligibility, process, and status guidance for refunds.
- **Main sections:** scope; eligibility; exclusions; request process; evidence
  requirements; refund method; refund status; exceptions and escalation.
- **Required information:** approved eligibility conditions, exclusions,
  required order evidence, request channels, refund destination rules, status
  definitions, and exception owner. Team confirmation is required for all
  refund windows, fees, partial-refund rules, and processing times.
- **Expected content:** controlled policy statements and process steps. It must
  distinguish a refund request from approval and from receipt of funds.
- **Arabic and English:** policy conditions and exceptions must be legally
  reviewed in both languages; both versions must use the same version and
  effective date.
- **Source and ownership:** finance and customer-policy owner are accountable;
  legal/compliance and support approve publication.
- **RAG integration:** tag with `category=payment`; preserve section-level
  citations for eligibility and status answers; require human review for an
  exception, incomplete evidence, or a rule not covered by the applicable
  market/version.

### 3.4 Shipping Policy

- **Proposed filename:** `shipping-policy.md`
- **Purpose:** Describe shipping availability, options, charges, and shipment
  conditions at a policy level.
- **Main sections:** scope and regions; shipping options; address requirements;
  charges; dispatch and delivery estimates; restrictions; changes and
  cancellations; lost or damaged shipments; escalation.
- **Required information:** supported regions, carriers or fulfilment channels,
  address rules, item restrictions, charge rules, estimate definitions, and
  ownership of shipment exceptions. Team confirmation is required for all fees,
  thresholds, cut-off times, and delivery estimates.
- **Expected content:** approved customer-facing terms, with explicit
  separation between an estimate and a guarantee.
- **Arabic and English:** equivalent names for shipment states and customer
  actions; region and carrier names must be accurate in both versions.
- **Source and ownership:** logistics/fulfilment owner is accountable;
  operations and support approve operational guidance.
- **RAG integration:** tag with `category=delivery`; chunk by region and topic;
  require region metadata at retrieval time and abstain when no matching region
  is available.

### 3.5 Order Tracking Guide

- **Proposed filename:** `order-tracking-guide.md`
- **Purpose:** Help customers find and interpret an order or shipment status
  without exposing internal fulfilment systems.
- **Main sections:** prerequisites; where to find an order number; tracking
  steps; status glossary; common issues; when to contact support; data privacy.
- **Required information:** supported tracking entry points, order-identifier
  format, approved status labels, safe troubleshooting steps, and escalation
  conditions. Team confirmation is required for exact portal paths, carrier
  integrations, and status-specific actions.
- **Expected content:** procedural guidance only; it must not promise a
  delivery date or reveal customer data.
- **Arabic and English:** mirror every step and status definition; verify UI
  labels against the customer-facing product in both languages.
- **Source and ownership:** fulfilment and support operations own the process;
  product owner validates UI instructions.
- **RAG integration:** tag with `category=delivery`; chunk each procedure and
  status definition separately; cite this guide with `shipping-policy.md` when
  both procedure and policy are needed.

### 3.6 Account Support

- **Proposed filename:** `account-support.md`
- **Purpose:** Provide approved self-service and escalation guidance for access
  and profile-management issues.
- **Main sections:** account access; password reset; account verification;
  profile updates; account security; deletion or closure requests; escalation.
- **Required information:** supported account actions, identity-verification
  boundary, secure recovery process, privacy-request workflow, and escalation
  owner. Team confirmation is required for authentication methods, retention
  rules, and deletion handling.
- **Expected content:** safe, user-visible steps. It must never request
  passwords, one-time codes, or other secrets.
- **Arabic and English:** pair all steps and security warnings; validate
  product-navigation terms in both languages.
- **Source and ownership:** identity/account product owner is accountable;
  security, privacy, and support approve their areas.
- **RAG integration:** tag with `category=account`; chunk by task; apply a
  safety rule that routes suspected account compromise or unsupported identity
  verification to a human agent.

### 3.7 Delivery Support

- **Proposed filename:** `delivery-support.md`
- **Purpose:** Give operational guidance for delivery incidents after shipment,
  including delays, failed delivery attempts, missing parcels, and damage.
- **Main sections:** delivery-status checks; delayed delivery; failed attempt;
  address issue; missing parcel; damaged item; proof of delivery; escalation.
- **Required information:** supported incident types, required customer/order
  information, approved status definitions, case-creation process, and
  escalation thresholds. Team confirmation is required for investigation
  timelines, compensation, redelivery, replacement, and carrier-specific rules.
- **Expected content:** diagnostic and handoff instructions. Any outcome that
  changes customer entitlement must defer to an approved policy.
- **Arabic and English:** equivalent incident names and instructions; use the
  same evidence and escalation requirements in both languages.
- **Source and ownership:** logistics support owner is accountable; fulfilment
  operations and customer support review it.
- **RAG integration:** tag with `category=delivery`; keep incident chunks
  separate from shipping-policy chunks; return citations and abstain when an
  entitlement or carrier rule is not documented.

### 3.8 Technical Support

- **Proposed filename:** `technical-support.md`
- **Purpose:** Support customers with approved troubleshooting for the web,
  mobile, and service experience.
- **Main sections:** supported platforms; basic troubleshooting; sign-in and
  feature issues; error reporting; known incidents; accessibility; escalation.
- **Required information:** supported versions/devices, approved diagnostic
  steps, information safe to collect, incident-status source, and escalation
  route. Team confirmation is required for supported-version policy, service
  status channel, and diagnostic-data retention.
- **Expected content:** low-risk troubleshooting that neither asks for secrets
  nor instructs customers to weaken device or account security.
- **Arabic and English:** provide equivalent technical steps and error-label
  explanations; retain exact product error strings when necessary.
- **Source and ownership:** engineering/support owner is accountable; security,
  accessibility, and support review their areas.
- **RAG integration:** tag with `category=technical`; chunk by platform and
  symptom; include platform/version metadata; route security incidents and
  undocumented errors to human support.

## 4. RAG publishing and retrieval requirements

1. Store approved source documents under `rag/kb/` using the filenames in this
   plan. Do not ingest drafts or a document without ownership and an effective
   date.
2. Parse Markdown headings into sections and preserve `filename`, `title`,
   `language`, `section`, `version`, `effective_date`, `owner`, `category`,
   `region`, and `source_reference` metadata where available.
3. Index Arabic and English sections independently while retaining a common
   document version. Retrieve in the detected/requested language first; a
   fallback-language answer requires explicit product approval and bilingual
   review.
4. Return only traceable source filenames and sections to the reply generator.
   If retrieval has no applicable, approved source, the system must abstain and
   direct the case to a human agent.
5. Re-index after an approved change, retain the prior version for audit, and
   test retrieval in English, Arabic MSA, and Egyptian Arabic before release.

## 5. Team confirmations required before content creation

- Business identity, markets, supported channels, and the authoritative source
  systems for policy text.
- Policy values and exceptions for payments, refunds, shipping, and delivery.
- Customer-facing product paths and supported platforms for account and
  technical guidance.
- Named accountable owners, legal/compliance review requirements, publication
  workflow, and review cadence.
- The RAG ingestion implementation, chunk-size strategy, embedding model,
  access controls, and citation format.
