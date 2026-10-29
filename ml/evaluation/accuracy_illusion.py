"""
Week 1 - Success Metrics Doc, Section 1
Proof: why accuracy alone misleads on imbalanced data.
Run from repo root:  python ml/evaluation/accuracy_illusion.py
No dependencies (pure Python).
"""

# 100 tickets: 90 payment, 10 delivery (simplified mirror of our 7.1x imbalance)
y_true = ["payment"] * 90 + ["delivery"] * 10

# The dummy model: predicts "payment" for everything, reads nothing
y_pred = ["payment"] * 100


def recall_for(true, pred, label):
    tp = sum(1 for t, p in zip(true, pred) if t == label and p == label)
    fn = sum(1 for t, p in zip(true, pred) if t == label and p != label)
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)
rec_payment = recall_for(y_true, y_pred, "payment")
rec_delivery = recall_for(y_true, y_pred, "delivery")
macro_recall = (rec_payment + rec_delivery) / 2

print("=== The Dummy Model: always predicts 'payment' ===")
print(f"Accuracy          : {accuracy:.0%}   <- looks great")
print(f"Recall (payment)  : {rec_payment:.0%}")
print(f"Recall (delivery) : {rec_delivery:.0%}   <- ZERO: not one caught")
print(f"Macro recall      : {macro_recall:.0%}   <- exposes the trick")