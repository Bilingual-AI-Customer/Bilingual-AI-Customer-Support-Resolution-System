# Contributing

## Branches

- `main`: محمي. التحديث بالـ PR بس، وبيتحدث عند كل Milestone.
- `develop`: التجميع اليومي. كل الـ features بتتدمج هنا.
- `feature/<track>-<desc>`: مثال `feature/ml-xlmr-baseline`.
  Tracks: `data`, `ml`, `rag`, `backend`, `front`.
- `fix/<desc>`: لإصلاح الأخطاء.

## Commits

`type(scope): message`

Types: `feat`, `fix`, `data`, `ml`, `docs`, `test`, `chore`

مثال: `data(split): add fixed train/val/test with seed 42`

## Pull Requests

- من `feature/*` إلى `develop`.
- لازم مراجعة من عضو واحد على الأقل قبل الدمج.
- PR صغير ومحدد أفضل من PR كبير.
- وصف سطرين: إيه اللي اتعمل وإزاي اتجرب.

## Rules

1. `data/splits/` ثابت بعد الأسبوع 3. ممنوع التعديل.
2. الداتا الخام وملفات `.env` ممنوع ترفع (الريبو Public).
3. كل تجربة موديل تتسجل في MLflow، مش بس في notebook.
4. أي تغيير في `docs/contracts/` لازم الفريق كله يعرف بيه.
5. فولدر `Front/` بيتنشر تلقائيًا على GitHub Pages عند أي push على `main`. اتأكد إن اللي هيوصل لـ `main` شغال.