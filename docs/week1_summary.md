# ملخص الأسبوع الأول - Bilingual AI Customer Support & Resolution System

**المسؤول:** هشام - العضو 2 (التقييم ونماذج ML)
**التاريخ:** 2026-10-29
**الفرع:** develop

## 1. لوحة الأسبوع
| البند | الحالة | ملاحظة |
|---|---|---|
| وثيقة المقاييس success_metrics.md | تم - v0.3 | الأقسام 1-4 كاملة |
| سكريبتات التقييم الأربعة | تم | ml/evaluation/ |
| داتا banking77 + المابينج 77-4 | تم | data/ |
| Baseline إنجليزي | تم | Macro F1 = 0.9375 |
| تقرير EDA | تم | docs/eda_banking77.md |
| العقدين | مسودة | محتاجين توقيع عضو 1 وعضو 4 |
| داتا عربي (ar-msa / ar-eg) | منتظرة | على العضو 1 |

## 2. كل الملفات اللي اتعملت
| المسار | وظيفته | Commit |
|---|---|---|
| docs/success_metrics.md | وثيقة المقاييس v0.3 | - |
| ml/evaluation/accuracy_illusion.py | إثبات خداع الـ Accuracy | ad07cdd |
| ml/evaluation/metrics_101.py | سيناريوهات P/R/F1 باليد | 0b0e647 |
| ml/evaluation/language_split_demo.py | ليه مندمجش اللغات في رقم واحد | a53983c |
| ml/evaluation/confidence_threshold_demo.py | فكرة بوابة الثقة (محاكاة) | 7057744 |
| ml/baseline/download_banking77.py | تحميل الداتا | 377b03e |
| ml/baseline/train_baseline.py | التدريب + البوابة + الـ scan | 9ef1191 |
| ml/baseline/results.md | أرقام الـ baseline | 9ef1191 |
| data/mapping_77_to_4.csv | المابينج 77-4 | 377b03e |
| ml/baseline/eda_banking77.py | سكريبت الـ EDA | (جديد) |
| docs/eda_banking77.md | تقرير الـ EDA | (جديد) |
| data/samples_per_category.json | أمثلة verbatim لكل فئة | (جديد) |
| docs/contracts/model_output_contract.md | عقد العضو 4 v1.1 | f181c04 |
| docs/contracts/unified_data_schema.md | عقد العضو 1 | f181c04 |

## 3. نتايج الـ Baseline (أرقام حقيقية - test n = 3,080)
- Macro F1 (المقياس الأساسي): **0.9375**
- Accuracy (للعرض فقط): 0.9568
- F1 لكل فئة: payment 0.98 / account 0.96 / technical 0.91 / delivery 0.90
- بوابة الثقة عند T = 0.80: تغطية 65.0% بدقة 99.5% (بخطأ 0.5%) وحمل بشري 35.0%
- جدول الـ scan الكامل (T من 0.50 لـ 0.90) بيتولد من train_baseline.py ومسجل في results.md

## 4. نموذج الـ Baseline
TF-IDF (1-2 grams, sublinear_tf, min_df=2) + Logistic Regression
(max_iter=1000, class_weight=balanced).
ليه LR: اتاخت لأنها قوية على TF-IDF وبتدي احتمالات نستخدمها في البوابة
(NB كمان بيدي احتمالات بس عادة أقل معايرة).

## 5. قرارات الأسبوع الموثقة
1. Accuracy للعرض فقط - مش قرارية (سكريبت الوهم: 90% accuracy من موديل أعمى).
2. Macro F1 هو المقياس الأساسي.
3. التقييم لكل لغة لوحدها (en / ar-msa / ar-eg) - ممنوع أرقام pooled للقرارات.
4. البوابة: auto ⇔ confidence >= T، وT = 0.80 مؤقتة (تتظبط على validation حقيقية).
5. حد أدنى 30 عينة لخلية لغة×فئة وإلا تتعلم "pilot".

## 6. المابينج والنوايا المبهمة (7)
المابينج الفعلي: payment 42 / account 16 / technical 11 / delivery 8.
قايمة المبهمة بقيت 7 بدل 6 والتفاصيل في docs/eda_banking77.md قسم 6.
أبرزها card_acceptance: أمثلتها عن أماكن قبول الكارت مش عن التوصيل
(مثال حي: "Do you have a list of businesses that accept this card?").
نقلها لـ account بينزل الـ Macro من 0.9375 لـ 0.9358 - فالقرار قرار
معنى ومؤجل لميتنج الفريق. وكمان get_disposable_virtual_card
وgetting_virtual_card مش "توصيل" فعلياً (الكارت الافتراضي بيتنشأ فوراً).

## 7. الدروس
1. Accuracy ممكن تكون خداعة - النموذج الأعمى جاب 90%.
2. مثال محاكاة: EN 89.9% مقابل AR 37.5% - الفصل اللغوي بيحول "محتاج شغل"
   لـ"العربي انهار - فيه شغل محدد".
3. قرارات العتبة من داتا حقيقية مش من هوا (الـ scan على test).

### 7.2 أرقام اللغة دي محاكاة توضيحية
أرقام EN 89.9 / AR 37.5 / Pooled 64.2 محاكاة توضيحية لفكرة الفصل اللغوي،
ومش قياس لموديل حقيقي - هتتبدل بنتايج فعلية لما داتا ar-eg توصل.

## 8. العقود
| العقد | الطرف التاني | الحالة |
|---|---|---|
| model_output_contract v1.1 | عضو 4 | هشام وقّع - استنى توقيع العضو 4 |
| unified_data_schema | عضو 1 | هشام وقّع - استنى توقيع العضو 1 |

## 9. المعلقات (للميتنج / الأسبوع الجاي)
1. توقيع العقدين من عضو 1 وعضو 4.
2. داتا ar-eg من العضو 1 (هدف 200 عينة، حد أدنى 120).
3. تأكيد ترخيص ArBanking77 (CC-BY-4.0).
4. قرار card_acceptance ومراجعة النوايا المبهمة السبعة.
5. عمل validation split قبل تجميد T النهائية.
6. ملف المعمارية architecture_ml_view.md - بعد الميتنج (مؤجل بقرار).
