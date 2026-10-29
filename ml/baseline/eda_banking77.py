"""
Week 1 - BANKING77 EDA (Exploratory Data Analysis)
Companion of: docs/eda_banking77.md
Run from repo root:  python ml/baseline/eda_banking77.py
Requires: pandas
Outputs:
  - console: report-ready tables (copy into docs/eda_banking77.md if numbers change)
  - data/samples_per_category.json: verbatim sample examples per category
"""
import json
from pathlib import Path

import pandas as pd

DATA = Path("data/banking77")
MAPPING = Path("data/mapping_77_to_4.csv")
OUT = Path("data/samples_per_category.json")
CATEGORIES = ["payment", "account", "technical", "delivery"]

# ---- analysis input: intents whose category assignment is debatable ----
# decision on these is deferred to the week-1 meeting (report Section 6/10)
AMBIGUOUS = [
    ("card_acceptance",             "delivery",  "about where the card is accepted - usage, not delivery"),
    ("get_disposable_virtual_card", "delivery",  "virtual card is issued instantly - nothing is delivered"),
    ("getting_virtual_card",        "delivery",  "same reason as above"),
    ("disposable_card_limits",      "technical", "product-limits question - closer to account"),
    ("atm_support",                 "technical", "ATM availability - usage question, closer to payment"),
    ("card_about_to_expire",        "account",   "renewal may involve a replacement card being delivered"),
    ("lost_or_stolen_card",         "technical", "security (technical), but the replacement card is delivered"),
]

train = pd.read_csv(DATA / "train.csv")
test = pd.read_csv(DATA / "test.csv")
names = json.loads((DATA / "label_names.json").read_text())
mapping = pd.read_csv(MAPPING)
intent_to_cat = dict(zip(mapping["intent"], mapping["category"]))

train["category"] = train["label"].map(lambda i: intent_to_cat[names[i]])
test["category"] = test["label"].map(lambda i: intent_to_cat[names[i]])

print("=" * 64)
print("BANKING77 EDA - Week 1")
print("=" * 64)
print(f"train rows : {len(train)}")
print(f"test rows  : {len(test)}")
print(f"intents    : {len(names)}")

print("\nCategory distribution (share of rows)")
print("| Category | Train | Test |")
print("|---|---:|---:|")
for c in CATEGORIES:
    tr = (train["category"] == c).mean() * 100
    te = (test["category"] == c).mean() * 100
    print(f"| {c:9s} | {tr:.1f}% | {te:.1f}% |")

print("\nIntents per category (from data/mapping_77_to_4.csv)")
print("| Category | Intents | Train rows |")
print("|---|---:|---:|")
for c in CATEGORIES:
    n = sum(1 for v in intent_to_cat.values() if v == c)
    rows = (train["category"] == c).sum()
    print(f"| {c:9s} | {n} | {rows} |")

all_support = train["label"].map(lambda i: names[i]).value_counts()
print(f"\nSupport per intent (train): min {all_support.min()}, "
      f"median {int(all_support.median())}, max {all_support.max()}")
print("Smallest intents:",
      ", ".join(f"{k} ({v})" for k, v in all_support.nsmallest(3).items()))

print("\nAmbiguous intents (7) - decision deferred to the meeting")
print("| Intent | Current category | Concern |")
print("|---|---|---|")
for it, cur, why in AMBIGUOUS:
    print(f"| {it} | {cur} | {why} |")
missing = [it for it, _, _ in AMBIGUOUS if it not in intent_to_cat]
assert not missing, f"Ambiguous intents missing from mapping: {missing}"

print("\nVerbatim samples per category (train.csv, copied as-is)")
print("| Category | Example (verbatim from train) | Original intent |")
print("|---|---|---|")
samples = {}
for c in CATEGORIES:
    sub = train[train["category"] == c].copy()
    sub["intent"] = sub["label"].map(lambda i: names[i])
    sub = sub[sub["text"].str.len().between(40, 120)]
    sub = sub[~sub["text"].str.contains("\n")]
    sub = sub.sort_values(["intent", "text"]).drop_duplicates("intent")
    picked, seen = [], set()
    for _, r in sub.iterrows():
        if r["intent"] in seen:
            continue
        seen.add(r["intent"])
        picked.append({"intent": r["intent"], "text": r["text"]})
        if len(picked) == 3:
            break
    samples[c] = picked
    for p in picked:
        print(f"| {c} | {p['text']} | {p['intent']} |")

OUT.write_text(json.dumps(samples, indent=2, ensure_ascii=False))
print(f"\nSaved: {OUT}")
