# -*- coding: utf-8 -*-
"""
build_egyptian_train.py
=======================
إغلاق مشاكل داتا العربي النهائية (Week 2 — Member 2):

  المدخل: download/eg_complaints_final.csv (25,576 صف — weak labels)
  المخرجات:
    1) download/eg_complaints_egy_train.csv   ملف التدريب المصري النهائي
       (سكيما موحدة: ticket_id / text / language / category / priority / status)
    2) download/eg_excluded_label_check.csv   كل الصفوف المستبعدة + السبب

القواعد (موثقة وقابلة لإعادة الإنتاج — دي هي "الإغلاق"):
  Step A — فلتر لهجة/جودة:
    A1 استبعاد نص أقصر من 15 حرف
    A2 استبعاد PII (إيميل / لينك / رقم 7 أرقام أو أكثر)
    A3 استبعاد أي صف فيه علامة لهجة غير مصرية (مغربي/خليجي/شامي)
    A4 اشتراط علامة مصرية قوية واحدة على الأقل
  Step B — تأكيد التصنيف بالأدلة:
    B1 الصف يحتفظ بتصنيفه لو فيه دليل قوي >=1 أو دليل ضعيف >=2 لفئته
    B2 وإلا: لو فئة تانية واحدة بس عليها دليل قوي -> إعادة تصنيف (label_source=reassigned)
    B3 تعادل أو مفيش دليل قوي لأي فئة -> استبعاد بسبب label_no_evidence / label_tie

  ملاحظة مهمة: النص نفسه مش بنعدل فيه حرف (السكيما بتقول raw text no pre-cleaning) —
  الفلتر بيختار الصفوف بس، مش بيعدل المحتوى.
"""
import os
import re
import sys
import argparse
import pandas as pd

CATS = ["payment", "account", "technical", "delivery"]

# ------------------------------------------------------------------
# Step A قوائم — علامات مصرية قوية / علامات لهجات تانية
# ------------------------------------------------------------------
EG_MARKERS = [
    "كده", "ده", "دي", "دول", "ايه", "فين", "ليه", "امتى", "عايز", "عاوز",
    "عايزين", "عاوزين", "بتاع", "بتوع", "خالص", "دلوقتي", "دلوقتى", "برضه",
    "برضو", "عشان", "كمان", "معلش", "طب", "بقاله", "بقالها", "ازاي", "إزاي",
    "عايزة", "عاوزة", "مش عارف", "من فترة", "من فتره",
]
DIALECT_EXCLUDE = {
    "مغربي": ["ديال", "ديالك", "ديالكم", "بزاف", "دابا", "والو", "مزيان",
              "غادي", "نيشان", "دوك", "كاين", "كاينة", "بغيت", "ديما",
              "هادشي", "هادي", r"مشكل(?!ة|ه)"],
    "خليجي": ["وين", "شنو", "شلون", "الحين", "ايش", "ليش", "وايد", "توه"],
    "شامي": ["هيك", "منيح", "هلق", "بدك", "بدنا", "فيي"],
}
PII_PATTERNS = [r"\S+@\S+\.\S+", r"https?://", r"www\.", r"\d{7,}"]

# ------------------------------------------------------------------
# Step B قوائم — أدلة الفئات (قوية / ضعيفة)
# ------------------------------------------------------------------
STRONG = {
    "payment": [
        "تحويل", "ايداع", "إيداع", "سحب", "خصم", "اتخصم", "اترحمني", "رحمني",
        "رصيد", "فلوس", "دفع", "ادفع", "فاتورة", "فواتير", "كاش", "محفظة",
        "محفظتي", "عمولة", "عمولات", "استرداد", "استرجاع", "refund",
        "ترانزاكشن", "حوالة", "فيزا", "ماستر", "بطاقة ائتمان", "card",
        "payment", "رسوم", "اتخصمت", "توب", "top up", "topup",
        "اقساط", "أقساط", "تقسيط", "تقسيطات", "قسط", "تسديد", "سداد",
        "كريدت", "قرض", "قروض", "تمويل", "قسطي", "القسط",
        "ضريبة", "ضريبه", "ضرايب", "ضرائب", "دافع", "مدفوع", "دفعت",
    ],
    "account": [
        "حساب", "تسجيل", "باسورد", "كلمة السر", "الرقم السري", "otp",
        "اوتي بي", "كود التحقق", "توثيق", "هويتي", "الرقم القومي",
        "بياناتي", "الايميل", "ايميلي", "البريد الالكتروني", "رقم الموبايل",
        "الرقم المرتبط", "profile", "account", "تغيير بياناتي", "تسجيل خروج",
        "مستخدم", "password", "قفلوا حسابي", "اغلاق الحساب", "عندي حساب",
    ],
    "technical": [
        "التطبيق", "تطبيقكم", "تطبيقك", "الابلكيشن", "ابلكيشن", "app", "طبيق",
        "بيقفل", "بيتقفل", "بيهنج", "هنح", "بطيء", "بطئ", "بطيئه", "بطيئة",
        "مش راضي يفتح", "مش بيتفتح", "مش راضي يشتغل", "بيعلق", "بيتجمد",
        "بيخرف", "بتخرف", "عطل", "معطل", "خطا", "خطأ", "error",
        "مش شغال", "مشكلة تقنية", "مشكله تقنيه", "تحديث", "احدثت", "نسخة",
        "كراش", "الشاشة", "سيرفر", "شبكة", "النت", "انترنت", "internet",
        "بج", "bug", "مش راضي يدخل", "بيطلعلي", "يرفض يفتح", "مظبوط",
        "ابليكشن", "مش بيفتح", "مش بيعمل",
        "برنامج", "الاشعارات", "إشعارات", "اشعارات", "رسائل التاكيد",
        "رسائل التأكيد", "ما بتجيش", "ما بتيجيش",
    ],
    "delivery": [
        "توصيل", "التوصيل", "شحنة", "الشحنة", "شحنات", "شحنت", "أوردر",
        "اوردر", "الاوردر", "الأوردر", "الطلبية", "الطلبيات", "وصلني",
        "وصلتني", "وصلنيش", "مجانيش", "مجاش", "ماجاش", "ماجاليش",
        "ملحقتش", "استلمت", "استلام", "المندوب", "مندوب", "الفارس",
        "فارس", "الكابتن", "كابتن", "البريد", "delivery", "shipping",
        "الشحنه", "شحنة", "الكارت مجاش", "الكارد مجاش", "الكرت مجاش", "طبيق",
    ],
}
WEAK = {
    "payment": ["معاملة", "معامله", "مصاريف", "خصومات", "شحن"],
    "account": ["بيانات", "دخول", "موبايلي", "كود", "بطاقه", "بطاقة",
                "بطاقتي", "البطاقه", "البطاقة", "كارت", "كرت", "كارد",
                "كارتي", "كرتي", "الكارت", "الكرت", "مسجل", "سجلت"],
    "technical": ["تحميل", "اتصال", "يفتح"],
    "delivery": ["طلبت", "الطلب", "طلباتي", "طلبي", "متأخر", "تأخير",
                 "متاخر", "تاخر", "توصل", "وصلني", "توصلي"],
}

STRONG_RE = {c: [re.compile(p) for p in pats] for c, pats in STRONG.items()}
WEAK_RE = {c: [re.compile(p) for p in pats] for c, pats in WEAK.items()}


def hits(regexes, text):
    return sum(1 for r in regexes if r.search(text))


def evidence(text):
    return {c: (hits(STRONG_RE[c], text), hits(WEAK_RE[c], text)) for c in CATS}


def main():
    # Windows consoles default to cp1256 and crash on emoji in the
    # sample prints. Both CSVs are already written; keep prints non-fatal.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/egyptian_reviews/eg_complaints_final.csv")
    ap.add_argument("--out-dir", default="data/egyptian_reviews")
    args = ap.parse_args()
    SRC = args.src
    OUT_TRAIN = os.path.join(args.out_dir, "eg_complaints_egy_train.csv")
    OUT_EXCL = os.path.join(args.out_dir, "eg_excluded_label_check.csv")

    df = pd.read_csv(SRC)
    df = df.rename(columns={"complaint_text": "text"})
    df["text"] = df["text"].astype(str).str.strip()
    df = df.reset_index(drop=True)
    df["ticket_id"] = [f"ar-eg-{i+1:06d}" for i in range(len(df))]

    excl = []  # (ticket_id, text, original_category, reason)

    # ---------------- Step A: فلتر اللهجة والجودة ----------------
    keep_rows, label_source = [], []
    for _, row in df.iterrows():
        t, cat = row["text"], row["category"]
        tid = row["ticket_id"]
        if len(t) < 15:
            excl.append((tid, t, cat, "short_text")); continue
        if any(re.search(p, t) for p in PII_PATTERNS):
            excl.append((tid, t, cat, "pii")); continue
        bad = None
        for dialect, pats in DIALECT_EXCLUDE.items():
            if any(re.search(p, t) for p in pats):
                bad = f"other_dialect_{dialect}"; break
        if bad:
            excl.append((tid, t, cat, bad)); continue
        if not any(m in t for m in EG_MARKERS):
            excl.append((tid, t, cat, "no_egyptian_marker")); continue
        keep_rows.append((tid, t, cat))

    # ---------------- Step B: تأكيد التصنيف بالأدلة ----------------
    train_rows, stats = [], {c: {"keep": 0, "reassigned": 0, "dropped": 0} for c in CATS}
    for tid, t, cat in keep_rows:
        ev = evidence(t)
        s_own, w_own = ev[cat]
        if s_own >= 1 or w_own >= 2:
            train_rows.append((tid, t, cat, "original"))
            stats[cat]["keep"] += 1
            continue
        # مفيش دليل كافي لفئته — نشوف لو فئة تانية عليها دليل قوي
        others = [(c, s) for c, (s, w) in ev.items() if c != cat and s >= 1]
        if len(others) == 1:
            new_cat = others[0][0]
            train_rows.append((tid, t, new_cat, "reassigned"))
            stats[cat]["reassigned"] += 1
        elif len(others) > 1:
            best = max(others, key=lambda x: x[1])
            runner = sorted((s for _, s in others), reverse=True)[1]
            if best[1] > runner:  # فايز بفارق واضح
                train_rows.append((tid, t, best[0], "reassigned"))
                stats[cat]["reassigned"] += 1
            else:
                excl.append((tid, t, cat, "label_tie"))
                stats[cat]["dropped"] += 1
        else:
            excl.append((tid, t, cat, "label_no_evidence"))
            stats[cat]["dropped"] += 1

    # ---------------- المخرجات ----------------
    train = pd.DataFrame(train_rows, columns=["ticket_id", "text", "category", "label_source"])
    train.insert(2, "language", "ar-eg")
    train["priority"] = ""
    train["status"] = ""
    train = train[["ticket_id", "text", "language", "category", "priority", "status", "label_source"]]
    train.to_csv(OUT_TRAIN, index=False, encoding="utf-8-sig")

    ex = pd.DataFrame(excl, columns=["ticket_id", "text", "original_category", "exclude_reason"])
    ex.to_csv(OUT_EXCL, index=False, encoding="utf-8-sig")

    # ---------------- التقرير ----------------
    print("=== Step A — فلتر اللهجة/الجودة ===")
    print(f"المصدر: {len(df)} | عدي بعد الفلتر: {len(keep_rows)} | مستبعد: {len(excl)}")
    print(ex["exclude_reason"].value_counts().to_string())
    print("\n=== Step B — تأكيد التصنيف ===")
    for c in CATS:
        s = stats[c]
        print(f"  {c:10s} keep={s['keep']:5d} reassigned={s['reassigned']:4d} dropped={s['dropped']:4d}")
    print("\n=== التوزيع النهائي لملف التدريب ===")
    print(train["category"].value_counts().to_string())
    print(f"\n[تم] {OUT_TRAIN} — {len(train)} صف")
    print(f"[تم] {OUT_EXCL} — {len(ex)} صف")
    print("\nعدد الصفوف لكل category (سطر التحقق حسب العقد §4):")
    vc = train["category"].value_counts()
    print(" / ".join(f"{c} {vc.get(c,0)}" for c in CATS))

    # عينات للفحص البصري
    print("\n=== عينات إعادة تصنيف (للفحص) ===")
    sample = train[train["label_source"] == "reassigned"].head(5)
    for _, r in sample.iterrows():
        print(f"  [{r['category']}] {r['text'][:90]}")
    print("\n=== عينات label_no_evidence (للفحص) ===")
    for _, r in ex[ex["exclude_reason"] == "label_no_evidence"].head(5).iterrows():
        print(f"  [{r['original_category']}] {str(r['text'])[:90]}")


if __name__ == "__main__":
    main()
