# DocMind AI

AI-powered document assistant — foydalanuvchi PDF/DOCX/TXT hujjatlarni yuklaydi, tizim ularni indekslaydi va ChatGPT uslubidagi suhbat orqali hujjat mazmuni bo'yicha savol-javob, xulosalash, tarjima va ma'lumot ajratib olishni taqdim etadi (RAG — Retrieval-Augmented Generation asosida).

## Holati

Loyiha faol ishlab chiqilmoqda. Hozirgi bosqich:

- [x] Auth: ro'yxatdan o'tish, login, JWT autentifikatsiya, `/me`
- [x] Hujjat yuklash (PDF/DOCX/TXT) + matn ajratish
- [x] Alembic migratsiyalari
- [x] Vue 3 frontend (login/register/dashboard/hujjatlar)
- [x] AI/RAG integratsiyasi (chunking, embedding, vector qidiruv, Q&A — Ollama + sentence-transformers)
- [x] Chat UI va tarix (hujjat bo'yicha bir nechta suhbat, xabarlar saqlanadi)
- [ ] Docker / production deploy

## Texnologiyalar

**Backend:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT (python-jose), Passlib (bcrypt), Pydantic, pypdf, python-docx

**Frontend:** Vue 3, TypeScript, Pinia, Vue Router, Axios, TailwindCSS

**AI:** Ollama (lokal LLM, standart model — `llama3.2`), Sentence Transformers (embedding), oddiy Postgres JSON ustunida saqlangan vektorlar + Python'da cosine similarity (pgvector emas — Windows'da o'rnatish qiyinligi sababli hozircha shunday)

## Loyiha strukturasi

```
docmind-ai/
├── backend/
│   ├── alembic/               # DB migratsiyalari
│   └── app/
│       ├── ai/                # Chunking, embedding, Ollama client, cosine similarity
│       ├── api/                # HTTP endpointlar (FastAPI routerlar)
│       ├── services/           # Biznes logika (shu jumladan QAService, ChatService)
│       ├── repositories/       # Ma'lumotlar bazasi bilan ishlash
│       ├── models/             # SQLAlchemy modellar
│       ├── schemas/            # Pydantic sxemalar (request/response)
│       ├── utils/              # Yordamchi funksiyalar (JWT, hash, matn ajratish)
│       ├── core/                # Konfiguratsiya
│       └── db/                  # DB session
└── frontend/
    └── src/
        ├── api/                # Axios client
        ├── components/         # Qayta ishlatiladigan komponentlar (AppHeader, PasswordInput)
        ├── pages/              # Sahifalar (Login/Register/Dashboard/Documents/Chat)
        ├── router/             # Vue Router + auth guard
        └── stores/             # Pinia store'lar (auth, documents, chat)
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

## AI (Ollama) sozlash

Hujjat bo'yicha savol-javob ishlashi uchun [Ollama](https://ollama.com) kompyuteringizda o'rnatilgan va ishlab turishi kerak:

```bash
ollama pull llama3.2
```

Boshqa model ishlatmoqchi bo'lsangiz, `.env`dagi `OLLAMA_MODEL`ni o'zgartiring (masalan o'zbek tilida sifatliroq javoblar uchun `qwen2.5`).

## Ishga tushirish (frontend)

```bash
cd frontend
npm install
copy .env.example .env      # va VITE_API_BASE_URL'ni tekshiring
npm run dev
```

Brauzerda `http://localhost:5173` ochiladi (backend ishlab turishi kerak).
