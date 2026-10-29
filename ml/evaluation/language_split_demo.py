"""
Week 1 - Success Metrics Doc, Section 3
Why metrics must be computed per language (EN vs AR split).
Run:  python ml/evaluation/language_split_demo.py
No dependencies (pure Python).
"""


def prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


# Mini test set: (language, true_category, predicted_category)
# English: healthy model. Arabic: same model, collapsed on Arabic.
rows = [
    ("en", "payment",  "payment"),
    ("en", "payment",  "payment"),
    ("en", "payment",  "payment"),
    ("en", "payment",  "payment"),
    ("en", "payment",  "payment"),
    ("en", "delivery", "delivery"),
    ("en", "delivery", "delivery"),
    ("en", "delivery", "delivery"),
    ("en", "delivery", "delivery"),
    ("en", "delivery", "payment"),
    ("ar", "payment",  "payment"),
    ("ar", "payment",  "payment"),
    ("ar", "payment",  "payment"),
    ("ar", "payment",  "delivery"),
    ("ar", "payment",  "delivery"),
    ("ar", "delivery", "delivery"),
    ("ar", "delivery", "payment"),
    ("ar", "delivery", "payment"),
    ("ar", "delivery", "payment"),
    ("ar", "delivery", "payment"),
]

CATS = ["payment", "delivery"]


def bucket_stats(subset):
    stats = {}
    f1s = []
    for cat in CATS:
        tp = sum(1 for _lang, t, p in subset if t == cat and p == cat)
        fp = sum(1 for _lang, t, p in subset if t != cat and p == cat)
        fn = sum(1 for _lang, t, p in subset if t == cat and p != cat)
        p_, r_, f_ = prf(tp, fp, fn)
        stats[cat] = (p_, r_, f_)
        f1s.append(f_)
    stats["macro"] = sum(f1s) / len(f1s)
    return stats


results = {
    "EN": bucket_stats([r for r in rows if r[0] == "en"]),
    "AR": bucket_stats([r for r in rows if r[0] == "ar"]),
    "POOLED": bucket_stats(rows),
}

print("Bucket   payment P/R/F1          delivery P/R/F1         MACRO F1")
print("-" * 72)
for name, s in results.items():
    pc, dc = s["payment"], s["delivery"]
    print(f"{name:<8} {pc[0]:.0%} / {pc[1]:.0%} / {pc[2]:.1%}      "
          f"{dc[0]:.0%} / {dc[1]:.0%} / {dc[2]:.1%}      {s['macro']:.1%}")
print("-" * 72)
print(f"Pooled {results['POOLED']['macro']:.1%} says 'needs work'.")
print(f"The split says: EN {results['EN']['macro']:.1%} healthy, "
      f"AR {results['AR']['macro']:.1%} collapsed -> actionable fix.")
