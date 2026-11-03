# Baseline Results (Week 1)

**Model:** TF-IDF (1-2 grams, sublinear) + Logistic Regression (class_weight=balanced)

**Data:** PolyAI/banking77 mapped to 4 categories via data/mapping_77_to_4.csv

**Language bucket:** en (Arabic buckets pending - doc 3.3)

- **Macro F1 (primary): 0.9375**
- Overall accuracy (reference only): 0.9568
- Confidence gate T=0.80: coverage 65.0%, accuracy on routed 0.9950

## Threshold scan (real, test n=3,080)

| T | Coverage | Accuracy on routed | Human load |
|---:|---:|---:|---:|
| 0.50 | 95.0% | 97.54% | 5.0% |
| 0.60 | 89.0% | 98.54% | 11.0% |
| 0.70 | 79.5% | 99.18% | 20.5% |
| 0.80 | 65.0% | 99.50% | 35.0% |
| 0.90 | 39.1% | 99.50% | 60.9% |

Gate decision: T=0.80 provisional (metrics doc 4.3).

## Per-class report

```
              precision    recall  f1-score   support

     account       0.96      0.96      0.96       640
    delivery       0.89      0.91      0.90       320
     payment       0.99      0.97      0.98      1680
   technical       0.89      0.92      0.91       440

    accuracy                           0.96      3080
   macro avg       0.93      0.94      0.94      3080
weighted avg       0.96      0.96      0.96      3080

```

---

## v2 Re-run — EN Baseline على المابينج النهائي

**السكريبت:** `train_baseline_v2.py` | **الإعدادات:** زي v1 بالظبط — TF-IDF (1-2 grams, sublinear_tf, min_df=2) + LogisticRegression (max_iter=1000, class_weight=balanced, random_state=42)

### Before / After

| المقياس | v1 (draft mapping) | v2 (final mapping) | الفرق |
|---|---|---|---|
| Macro F1 | 0.9375 | **0.9068** | -0.0307 |
| Accuracy | 0.9568 | 0.9477 | -0.0091 |
| F1 — payment | 0.98 | 0.96 | -0.02 |
| F1 — account | 0.96 | 0.95 | -0.01 |
| F1 — technical | 0.91 | 0.82 | -0.09 |
| F1 — delivery | 0.90 | 0.89 | -0.01 |
| Coverage @ T=0.80 | 65.0% | 66.0% | +1.0 pp |
| Accuracy على الموجه | 0.9950 | 0.9956 | +0.0006 |
| حمل بشري | 35.0% | 34.0% | -1.0 pp |

**توزيع test (v2):** payment 1800 / account 1000 / technical 200 / delivery 80

**فحص البوابات:** Macro F1 PASS — أقل فئة PASS
**أكتر تنبيكات:** payment->technical (51), account->payment (33), payment->account (30)
**تشخيص needs_review:** Macro F1 على النيات المطموءة = 0.9220 (2520 صف) مقابل 0.6493 على نيات needs_review (560 صف) — بيوّج قرار تعليم الـ 14 نية.

