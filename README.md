# Bilingual AI Customer Support & Resolution System

نظام دعم عملاء ثنائي اللغة (عربي / إنجليزي): يصنّف الشكوى، يحدد أولويتها، يسترجع السياسة المناسبة، ويجهز رد مقترح بمصادره. الموظف هو صاحب القرار النهائي.

## Structure

| Folder | Content | Track |
|---|---|---|
| `data/` | raw / processed / splits (الـ splits ثابتة بعد الأسبوع 3) | Data |
| `ml/` | preprocessing, baseline, models, evaluation | Data, ML |
| `rag/` | knowledge base (`kb/`), chunking, retrieval, agent | RAG |
| `backend/` | FastAPI + database + tests | Backend |
| `Front/` | web dashboard (HTML/CSS/JS), deployed to GitHub Pages | Frontend |
| `docs/` | problem definition, architecture, API contracts, reports | All |

## Status

- [ ] Week 1: Problem + Data + Skeleton
- [ ] Week 2: Data Prep
- [ ] Week 3: Baseline + Fixed Split

## Team workflow

Branches: `main` (protected) ← `develop` ← `feature/<track>-<desc>`
Commits: `type(scope): message`, where type is one of feat, fix, data, ml, docs, test, chore.