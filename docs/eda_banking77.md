# BANKING77 EDA Report (Week 1)

**Owner:** Hesham - Member 2 (Evaluation & ML Models)
**Date:** 2026-10-29
**Data:** data/banking77/ (PolyAI/banking77, CC-BY-4.0) + data/mapping_77_to_4.csv
**Script:** ml/baseline/eda_banking77.py (writes data/samples_per_category.json)

## 1. Purpose
Before trusting the baseline, we need to know what the data actually
looks like: sizes, class balance, intent support, and whether the
77-to-4 mapping produces sane categories. Every number in this report
is produced by the script above - no hand-typed statistics.

## 2. Dataset files
| File | Rows | Note |
|---|---:|---|
| data/banking77/train.csv | 10,003 | official BANKING77 train split |
| data/banking77/test.csv | 3,080 | official BANKING77 test split |
| data/banking77/label_names.json | 77 | intent names (index -> name) |
| data/mapping_77_to_4.csv | 77 | our mapping (intent -> category) |

## 3. Category distribution
| Category | Train | Test |
|---|---:|---:|
| payment   | 61.9% | 54.5% |
| account   | 19.4% | 20.8% |
| technical | 10.0% | 14.3% |
| delivery  | 8.7%  | 10.4% |

Note: test is less imbalanced than train (payment 54.5% vs 61.9%).
The imbalance argument (success_metrics 1.2) is stated on the training
distribution and still holds; week-1 metrics use the official test set.

## 4. Intents per category (77 -> 4)
| Category | Intents | Train rows |
|---|---:|---:|
| payment   | 42 | 6,190 |
| account   | 16 | 1,939 |
| technical | 11 | 1,000 |
| delivery  | 8  | 874 |

## 5. Support per intent
min 35, median 127, max 187. Smallest: contactless_not_working (35),
virtual_card_not_working (41), card_acceptance (59). No intent is
starved; the minimum (35) is above the 30-sample support rule in
success_metrics Section 3.2.

## 6. Ambiguous intents (7) - decision deferred to the meeting
| Intent | Current category | Concern |
|---|---|---|
| card_acceptance | delivery | about where the card is accepted - usage, not delivery |
| get_disposable_virtual_card | delivery | virtual card is issued instantly - nothing is delivered |
| getting_virtual_card | delivery | same reason as above |
| disposable_card_limits | technical | product-limits question - closer to account |
| atm_support | technical | ATM availability - usage question, closer to payment |
| card_about_to_expire | account | renewal may involve a replacement card being delivered |
| lost_or_stolen_card | technical | security (technical), but the replacement card is delivered |

card_acceptance is the addition raised in review: real examples like
"Do you have a list of businesses that accept this card?" are about
acceptance, not delivery. The list is 7 items (previously counted 6).

## 7. Sample examples per draft category (verbatim from train)
All rows below are extracted verbatim by the script into
data/samples_per_category.json - document and code output cannot drift.

| Category | Example (verbatim from train) | Original intent |
|---|---|---|
| payment | A refund for a recent return has not arrived on my card. | Refund_not_showing_up |
| payment | Am I able to do top-ups with Google Pay? | apple_pay_or_google_pay |
| payment | Are there any hidden limit on the auto top-up? | automatic_top_up |
| account | Can I get some help activating my new card? | activate_my_card |
| account | Am I able to open an account for my children? | age_limit |
| account | Are there any express fees if i want my new card faster? | card_about_to_expire |
| technical | Am I limited to what ATM I can use my card? | atm_support |
| technical | Can I add a card that I just found (again) to the app? | card_linking |
| technical | Can you help me with my card, I think it's broke. | card_not_working |
| delivery | Any place that takes Mastercard would be fine. | card_acceptance |
| delivery | 2 weeks ago I ordered my new card.  It isn't here.  What should I do? | card_arrival |
| delivery | Are the delivery days flexible?  My schedule only allows me to be a available on specific dates. | card_delivery_estimate |

## 8. Mapping impact notes
- Moving card_acceptance (delivery -> account) and re-training gives
  Macro F1 0.9358 vs 0.9375 - a meaning decision, not a numbers
  decision, so it goes to the week-1 meeting. Until then the mapping
  stays as-is and ml/baseline/results.md remains valid.
- get_disposable_virtual_card / getting_virtual_card: same open
  question (virtual cards involve no physical delivery).

## 9. Reproduction
Run from the repo root:
    python ml/baseline/eda_banking77.py       # this report's numbers
    python ml/baseline/download_banking77.py  # original data download
    python ml/baseline/train_baseline.py      # baseline + threshold scan

## 10. Open questions for the week-1 meeting
1. card_acceptance: delivery vs account (acceptance meaning)?
2. get_disposable_virtual_card / getting_virtual_card: stay in delivery?
3. disposable_card_limits / atm_support: technical or account/payment?
4. Train/test distribution shift: acceptable for week 1; revisit when
   the validation split exists.
