# -*- coding: utf-8 -*-
"""
train_baseline_v2.py
====================
Week 2 — Task 9: EN baseline RE-RUN on mapping v2 (final datasets).

نفس إعدادات الـ baseline بتاع الأسبوع الأول بالظبط (TF-IDF + Logistic
Regression) — الفرق الوحيد إنه بيشتغل على الداتا النهائية بعد المابينج v2
(train_mapped_final.csv / test_mapped_final.csv) عشان نطلع أرقام قبل/بعد.

Run (from repo root):
    python ml/baseline/train_baseline_v2.py

Inputs (defaults — ممكن تتغير بـ args):
    --train   data/banking77/train_mapped_final.csv
    --test    data/banking77/test_mapped_final.csv
    --mapping data/banking77_intents_to_categories.csv
    --out     ml/baseline/results_v2_run.md

المخرجات:
    1) كل الأرقام على الشاشة (Macro F1 + per-class + بوابة T=0.80 + before/after)
    2) ملف markdown جاهز للصق في ml/baseline/results.md
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

# عشان الـ console على Windows ما يبوظش مع الحروف العربية
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RANDOM_STATE = 42
CATEGORIES = ["payment", "account", "technical", "delivery"]
T = 0.80  # بوابة الثقة المعتمدة في العقد

# أرقام v1 الموثقة في results.md (commit 9ef1191) — للمقارنة before/after
V1_REF = {
    "macro_f1": 0.9375,
    "accuracy": 0.9568,
    "per_class_f1": {"payment": 0.98, "account": 0.96, "technical": 0.91, "delivery": 0.90},
    "test_dist": {"payment": 1680, "account": 640, "technical": 440, "delivery": 320},
    "gate": {"coverage": 0.650, "acc_on_routed": 0.9950, "human_load": 0.350},
}

# البوابات المعتمدة (success_metrics.md)
GATES = {"macro_f1_en": 0.80, "min_class_f1": 0.60}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/banking77/train_mapped_final.csv")
    ap.add_argument("--test", default="data/banking77/test_mapped_final.csv")
    ap.add_argument("--mapping", default="data/banking77_intents_to_categories.csv")
    ap.add_argument("--out", default="ml/baseline/results_v2_run.md")
    args = ap.parse_args()

    for p in (args.train, args.test, args.mapping):
        if not Path(p).is_file():
            print(f"[خطأ] الملف مش موجود: {p}")
            print("شغّل السكريبت من جذر الريبو، وتأكد إن فرع الداتا فيه ملفات banking77.")
            sys.exit(1)

    # ---------- 1) تحميل الداتا المapped النهائية ----------
    train_df = pd.read_csv(args.train, encoding="utf-8-sig")
    test_df = pd.read_csv(args.test, encoding="utf-8-sig")
    for df, name in ((train_df, "train"), (test_df, "test")):
        missing = {"text", "intent", "category"} - set(df.columns)
        assert not missing, f"{name}: أعمدة ناقصة {missing}"

    mapping = pd.read_csv(args.mapping, encoding="utf-8-sig").set_index("intent")
    flagged = set(mapping.index[mapping["needs_review"] == "yes"])
    assert len(flagged) == 14, f"متوقع 14 نية needs_review، لقيت {len(flagged)}"

    print(f"Train: {len(train_df)} | Test: {len(test_df)}")
    test_dist = test_df["category"].value_counts().to_dict()
    print("توزيع test (v2):")
    for c in CATEGORIES:
        print(f"  {c:10s}: {test_dist.get(c, 0)}   (v1 كان: {V1_REF['test_dist'][c]})")
    nr_test = test_df["intent"].isin(flagged).sum()
    print(f"صفوف test جوا نيات needs_review (للتشخيص بس): {nr_test}")

    # ---------- 2) نفس إعدادات v1 بالظبط ----------
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2)
    X_train = vec.fit_transform(train_df["text"])
    X_test = vec.transform(test_df["text"])

    clf = LogisticRegression(max_iter=1000, class_weight="balanced",
                             random_state=RANDOM_STATE)
    clf.fit(X_train, train_df["category"])

    # ---------- 3) التقييم ----------
    y_test = test_df["category"]
    pred = clf.predict(X_test)
    proba = clf.predict_proba(X_test)

    acc = accuracy_score(y_test, pred)
    macro_f1 = f1_score(y_test, pred, average="macro")
    per_class = dict(zip(clf.classes_, f1_score(y_test, pred, average=None).round(4)))

    print("\n=== نتايج الـ Baseline v2 (إنجليزي — mapping v2) ===")
    print(f"Accuracy : {acc:.4f}   (v1: {V1_REF['accuracy']:.4f})")
    print(f"Macro F1 : {macro_f1:.4f}   (v1: {V1_REF['macro_f1']:.4f})")
    print("\nF1 لكل فئة (v2 مقابل v1):")
    for c in CATEGORIES:
        print(f"  {c:10s} {per_class[c]:.2f}   (v1: {V1_REF['per_class_f1'][c]:.2f})")
    print()
    print(classification_report(y_test, pred, digits=2))

    # ---------- 4) البوابات المعتمدة ----------
    ok_macro = macro_f1 >= GATES["macro_f1_en"]
    weak = {c: per_class[c] for c in CATEGORIES if per_class[c] < GATES["min_class_f1"]}
    print("=== فحص البوابات ===")
    print(f"Macro F1 >= {GATES['macro_f1_en']:.2f} : {'PASS' if ok_macro else 'FAIL'}")
    print(f"أقل فئة >= {GATES['min_class_f1']:.2f} : "
          f"{'PASS' if not weak else 'FAIL — ' + ', '.join(f'{c} ({f:.2f})' for c, f in weak.items())}")

    # ---------- 5) بوابة الثقة T=0.80 ----------
    conf = proba.max(axis=1)
    routed = conf >= T
    cov = routed.mean()
    acc_routed = (pred[routed] == y_test.values[routed]).mean() if routed.any() else float("nan")
    human = (~routed).mean()
    print(f"\n=== بوابة الثقة T={T:.2f} ===")
    print(f"Coverage            : {cov:.1%}   (v1: {V1_REF['gate']['coverage']:.1%})")
    print(f"Accuracy على الموجه : {acc_routed:.4f}   (v1: {V1_REF['gate']['acc_on_routed']:.4f})")
    print(f"حمل بشري            : {human:.1%}   (v1: {V1_REF['gate']['human_load']:.1%})")

    # ---------- 6) أكتر التنبيكات تكرار (تشخيص) ----------
    cm = confusion_matrix(y_test, pred, labels=CATEGORIES)
    pairs = []
    for i, true_c in enumerate(CATEGORIES):
        for j, pred_c in enumerate(CATEGORIES):
            if i != j and cm[i, j] > 0:
                pairs.append((cm[i, j], true_c, pred_c))
    pairs.sort(reverse=True)
    print("\nأكتر 5 تنبيكات (الحقيقة -> التوقع):")
    for n, true_c, pred_c in pairs[:5]:
        print(f"  {true_c} -> {pred_c}: {n}")

    # ---------- 7) تشخيص نيات needs_review ----------
    mask_ok = ~test_df["intent"].isin(flagged)
    if mask_ok.any() and (~mask_ok).any():
        f1_ok = f1_score(y_test[mask_ok], pred[mask_ok], average="macro")
        f1_nr = f1_score(y_test[~mask_ok], pred[~mask_ok], average="macro")
        print(f"\n=== تشخيص needs_review ===")
        print(f"Macro F1 على النيات المطموءة ({mask_ok.sum()} صف)   : {f1_ok:.4f}")
        print(f"Macro F1 على نيات needs_review ({(~mask_ok).sum()} صف): {f1_nr:.4f}")

    # ---------- 8) ملف markdown جاهز للصق ----------
    lines = []
    lines.append("## v2 Re-run — EN Baseline على المابينج النهائي")
    lines.append("")
    lines.append("**السكريبت:** `train_baseline_v2.py` | **الإعدادات:** زي v1 بالظبط — "
                 "TF-IDF (1-2 grams, sublinear_tf, min_df=2) + LogisticRegression "
                 f"(max_iter=1000, class_weight=balanced, random_state={RANDOM_STATE})")
    lines.append("")
    lines.append("### Before / After")
    lines.append("")
    lines.append("| المقياس | v1 (draft mapping) | v2 (final mapping) | الفرق |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Macro F1 | {V1_REF['macro_f1']:.4f} | **{macro_f1:.4f}** | {macro_f1 - V1_REF['macro_f1']:+.4f} |")
    lines.append(f"| Accuracy | {V1_REF['accuracy']:.4f} | {acc:.4f} | {acc - V1_REF['accuracy']:+.4f} |")
    for c in CATEGORIES:
        lines.append(f"| F1 — {c} | {V1_REF['per_class_f1'][c]:.2f} | {per_class[c]:.2f} "
                     f"| {per_class[c] - V1_REF['per_class_f1'][c]:+.2f} |")
    lines.append(f"| Coverage @ T=0.80 | {V1_REF['gate']['coverage']:.1%} | {cov:.1%} "
                 f"| {(cov - V1_REF['gate']['coverage']) * 100:+.1f} pp |")
    lines.append(f"| Accuracy على الموجه | {V1_REF['gate']['acc_on_routed']:.4f} | {acc_routed:.4f} "
                 f"| {acc_routed - V1_REF['gate']['acc_on_routed']:+.4f} |")
    lines.append(f"| حمل بشري | {V1_REF['gate']['human_load']:.1%} | {human:.1%} "
                 f"| {(human - V1_REF['gate']['human_load']) * 100:+.1f} pp |")
    lines.append("")
    lines.append(f"**توزيع test (v2):** " +
                 " / ".join(f"{c} {test_dist.get(c, 0)}" for c in CATEGORIES))
    lines.append("")
    lines.append("**فحص البوابات:** "
                 f"Macro F1 {'PASS' if ok_macro else 'FAIL'} — "
                 f"أقل فئة {'PASS' if not weak else 'FAIL (' + ', '.join(f'{c} {f:.2f}' for c, f in weak.items()) + ')'}")
    if pairs:
        top = ", ".join(f"{a}->{b} ({n})" for n, a, b in pairs[:3])
        lines.append(f"**أكتر تنبيكات:** {top}")
    try:
        lines.append(f"**تشخيص needs_review:** Macro F1 على النيات المطموءة = {f1_ok:.4f} "
                     f"({int(mask_ok.sum())} صف) مقابل {f1_nr:.4f} على نيات needs_review "
                     f"({int((~mask_ok).sum())} صف) — بيوّج قرار تعليم الـ 14 نية.")
    except NameError:
        pass
    lines.append("")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[تم] القسم الجاهز للصق في results.md اتكتب في: {out}")


if __name__ == "__main__":
    main()
