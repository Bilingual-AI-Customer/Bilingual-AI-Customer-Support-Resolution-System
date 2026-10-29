"""
Week 1 - Success Metrics Doc, Section 4
Confidence threshold and human handoff - choosing T with data.
Run:  python ml/evaluation/confidence_threshold_demo.py
No dependencies (pure Python).
"""

# Validation run bucketed by model confidence (simulated for demo):
# (bin_low, bin_high, n_predictions, n_correct)
buckets = [
    (0.90, 1.00, 100, 95),   # accuracy 95.0%
    (0.80, 0.90,  80, 70),   # accuracy 87.5%
    (0.70, 0.80,  60, 42),   # accuracy 70.0%
    (0.50, 0.70, 100, 50),   # accuracy 50.0%  <- coin-flip zone
]

total = sum(b[2] for b in buckets)
total_correct = sum(b[3] for b in buckets)

print("Confidence bin   Tickets   Accuracy")
print("-" * 40)
for low, high, n, c in buckets:
    print(f"{low:.2f}-{high:.2f}      {n:>5}     {c / n:.1%}")
print("-" * 40)
print(f"Overall          {total:>5}     {total_correct / total:.1%}")
print()

TARGET = 0.90
print("T      Coverage   Accuracy on routed")
print("-" * 40)
chosen = None
for t in [0.50, 0.60, 0.70, 0.80, 0.90]:
    n = sum(b[2] for b in buckets if b[0] >= t)
    c = sum(b[3] for b in buckets if b[0] >= t)
    acc = c / n if n else 0.0
    cov = n / total
    print(f"{t:.2f}   {cov:>7.1%}   {acc:>9.1%}")
    if chosen is None and acc >= TARGET:
        chosen = (t, cov, acc)

print("-" * 40)
if chosen:
    t, cov, acc = chosen
    print(f"Decision: T = {t:.2f} -> auto-route {cov:.1%} of tickets "
          f"at {acc:.1%} accuracy; the rest goes to humans.")