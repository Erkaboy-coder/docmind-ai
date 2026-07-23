# DocMind AI

AI-powered document assistant — foydalanuvchi PDF/DOCX/TXT hujjatlarni yuklaydi, tizim ularni indekslaydi va ChatGPT uslubidagi suhbat orqali hujjat mazmuni bo'yicha savol-javob, xulosalash, tarjima va ma'lumot ajratib olishni taqdim etadi (RAG — Retrieval-Augmented Generation asosida).

## Holati

Loyiha faol ishlab chiqilmoqda. Hozirgi bosqich:

- [x] Auth: ro'yxatdan o'tish, login, JWT autentifikatsiya, `/me`
- [x] Chat/Message modellari (ma'lumotlar bazasi darajasida)
- [x] Hujjat yuklash (PDF/DOCX/TXT) + matn ajratish
- [x] Alembic migratsiyalari
- [x] Vue 3 frontend (login/register/dashboard/hujjatlar)
- [ ] AI/RAG integratsiyasi (embedding, vector search, Q&A)
- [ ] Chat UI va tarix
- [ ] Docker / production deploy

## Texnologiyalar

**Backend:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT (python-jose), Passlib (bcrypt), Pydantic, pypdf, python-docx

**Frontend:** Vue 3, TypeScript, Pinia, Vue Router, Axios, TailwindCSS

**AI (rejalashtirilgan):** LangChain / LlamaIndex, OpenAI API yoki lokal LLM (Ollama), Sentence Transformers, pgvector

## Loyiha strukturasi

```
docmind-ai/
├── backend/
│   ├── alembic/             # DB migratsiyalari
│   └── app/
│       ├── api/              # HTTP endpointlar (FastAPI routerlar)
│       ├── services/         # Biznes logika
│       ├── repositories/     # Ma'lumotlar bazasi bilan ishlash
│       ├── models/           # SQLAlchemy modellar
│       ├── schemas/          # Pydantic sxemalar (request/response)
│       ├── utils/            # Yordamchi funksiyalar (JWT, hash, matn ajratish)
│       ├── core/              # Konfiguratsiya
│       └── db/                # DB session
└── frontend/
    └── src/
        ├── api/              # Axios client
        ├── components/       # Qayta ishlatiladigan komponentlar
        ├── pages/            # Sahifalar (Login/Register/Dashboard/Documents)
        ├── router/           # Vue Router + auth guard
        └── stores/           # Pinia store'lar (auth, documents)
```

## Ishga tushirish (backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

copy .env.example .env      # va qiymatlarni to'ldiring
```

PostgreSQL'da `.env`dagi `DATABASE_NAME` bilan mos baza yarating, so'ng migratsiyalarni qo'llang va serverni ishga tushiring:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API hujjatlari `http://localhost:8000/docs` manzilida ochiladi. Modelga o'zgartirish kiritganingizda, yangi migratsiya yarating:

```bash
alembic revision --autogenerate -m "tavsif"
alembic upgrade head
```

## Ishga tushirish (frontend)

```bash
cd frontend
npm install
copy .env.example .env      # va VITE_API_BASE_URL'ni tekshiring
npm run dev
```

Brauzerda `http://localhost:5173` ochiladi (backend ishlab turishi kerak).
