"""
Week 1 - Baseline: TF-IDF + Logistic Regression on BANKING77
mapped to the 4 project categories.

Evaluates exactly per docs/success_metrics.md:
  - Macro F1 (primary) + per-class Precision/Recall
  - Language bucket: en (ar-msa / ar-eg pending data - doc 3.3)
  - Confidence gate T=0.80: coverage & accuracy on auto-routed (doc 4)

Run from repo root:  python ml/baseline/train_baseline.py
Requires: python -m pip install pandas scikit-learn
"""
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import make_pipeline

DATA = Path("data/banking77")
OUT = Path("ml/baseline")
CATEGORIES = ["account", "delivery", "payment", "technical"]
T = 0.80  # provisional threshold - metrics doc Section 4

# ---------- load ----------
train = pd.read_csv(DATA / "train.csv")
test = pd.read_csv(DATA / "test.csv")
names = json.loads((DATA / "label_names.json").read_text())
mapping = pd.read_csv(Path("data/mapping_77_to_4.csv"))

intent_to_cat = dict(zip(mapping["intent"], mapping["category"]))
missing = [n for n in names if n not in intent_to_cat]
assert not missing, f"Intents missing from mapping: {missing}"

train["category"] = train["label"].map(lambda i: intent_to_cat[names[i]])
test["category"] = test["label"].map(lambda i: intent_to_cat[names[i]])

print(f"Train: {len(train)} rows | Test: {len(test)} rows")
print("Category distribution (test):")
print(test["category"].value_counts().to_string())

# ---------- train ----------
print("\nTraining TF-IDF + Logistic Regression (balanced)...")
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(train["text"], train["category"])

# ---------- evaluate ----------
y_true = test["category"].to_numpy()
pred = model.predict(test["text"])
proba = model.predict_proba(test["text"])

macro_f1 = f1_score(y_true, pred, labels=CATEGORIES, average="macro")
overall_acc = (pred == y_true).mean()

print()
print("=" * 60)
print("LANGUAGE BUCKET: en (all BANKING77 rows are English)")
print("=" * 60)
print(f"MACRO F1 (primary metric)  : {macro_f1:.4f}")
print(f"Overall accuracy (ref only): {overall_acc:.4f}")
print()
print("Per-class report (metrics doc Section 2 view):")
print(classification_report(y_true, pred, labels=CATEGORIES,
                            zero_division=0))

# ---------- confidence gate (metrics doc Section 4) ----------
confidence = proba.max(axis=1)
routed = confidence >= T
is_correct = pred == y_true
coverage = routed.mean()
routed_acc = is_correct[routed].mean() if routed.any() else 0.0

print("=" * 60)
print(f"CONFIDENCE GATE (T = {T:.2f})")
print("=" * 60)
print(f"Coverage (auto-routed)  : {coverage:.1%}")
print(f"Accuracy on routed      : {routed_acc:.4f}")
print(f"Human review load       : {(~routed).mean():.1%}")

# ---------- save evidence ----------
report = classification_report(y_true, pred, labels=CATEGORIES,
                               zero_division=0)
lines = [
    "# Baseline Results (Week 1)\n",
    "\n**Model:** TF-IDF (1-2 grams, sublinear) + Logistic Regression",
    " (class_weight=balanced)\n",
    "\n**Data:** PolyAI/banking77 mapped to 4 categories via",
    " data/mapping_77_to_4.csv\n",
    "\n**Language bucket:** en (Arabic buckets pending - doc 3.3)\n",
    f"\n- **Macro F1 (primary): {macro_f1:.4f}**\n",
    f"- Overall accuracy (reference only): {overall_acc:.4f}\n",
    f"- Confidence gate T={T:.2f}: coverage {coverage:.1%},",
    f" accuracy on routed {routed_acc:.4f}\n",
    "\n## Per-class report\n\n```\n", report, "\n```\n",
]
(OUT / "results.md").write_text("".join(lines))
print(f"\nSaved: {OUT / 'results.md'}")