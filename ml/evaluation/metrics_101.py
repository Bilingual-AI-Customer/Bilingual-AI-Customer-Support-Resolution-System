"""
Week 1 - Success Metrics Doc, Section 2
Precision / Recall / F1 by hand - scenarios A to D.
Run:  python ml/evaluation/metrics_101.py
No dependencies (pure Python).
"""


def prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


scenarios = [
    # (name, tp, fp, fn)
    ("A. Balanced catch",         12,  3,  8),   # P 80% R 60%
    ("B. Precision trap",          5,  0, 15),   # P100% R 25%
    ("C. Recall trap",            20, 15,  0),   # P 57% R100%
    ("D. Dummy model - payment",  90, 10,  0),   # P 90% R100%
    ("D. Dummy model - delivery",  0,  0, 10),   # all zero
]

print("Scenario                        Precision  Recall   F1")
print("-" * 55)
rows = []
for name, tp, fp, fn in scenarios:
    p, r, f = prf(tp, fp, fn)
    rows.append((name, p, r, f))
    print(f"{name:<30} {p:>8.0%} {r:>7.0%} {f:>7.1%}")

macro_f1 = (rows[3][3] + rows[4][3]) / 2
print("-" * 55)
print(f"Dummy model MACRO F1 : {macro_f1:.1%}   <- the honest number")
print("Dummy model MICRO F1 : 90.0%   <- the Section-1 accuracy trick again")