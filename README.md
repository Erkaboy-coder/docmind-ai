# DocMind AI

AI-powered document assistant — foydalanuvchi PDF/DOCX/TXT hujjatlarni yuklaydi, tizim ularni indekslaydi va ChatGPT uslubidagi suhbat orqali hujjat mazmuni bo'yicha savol-javob, xulosalash, tarjima va ma'lumot ajratib olishni taqdim etadi (RAG — Retrieval-Augmented Generation asosida).

## Holati

Loyiha faol ishlab chiqilmoqda. Hozirgi bosqich:

- [x] Auth: ro'yxatdan o'tish, login, JWT autentifikatsiya, `/me`
- [x] Chat/Message modellari (ma'lumotlar bazasi darajasida)
- [ ] Hujjat yuklash (PDF/DOCX/TXT)
- [ ] AI/RAG integratsiyasi (embedding, vector search, Q&A)
- [ ] Chat UI va tarix
- [ ] Vue 3 frontend
- [ ] Docker / production deploy

## Texnologiyalar

**Backend:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT (python-jose), Passlib (bcrypt), Pydantic

**Frontend (rejalashtirilgan):** Vue 3, TypeScript, Pinia, Vue Router, Axios, TailwindCSS

**AI (rejalashtirilgan):** LangChain / LlamaIndex, OpenAI API yoki lokal LLM (Ollama), Sentence Transformers, pgvector

## Loyiha strukturasi

```
docmind-ai/
├── backend/
│   └── app/
│       ├── api/            # HTTP endpointlar (FastAPI routerlar)
│       ├── services/       # Biznes logika
│       ├── repositories/   # Ma'lumotlar bazasi bilan ishlash
│       ├── models/         # SQLAlchemy modellar
│       ├── schemas/        # Pydantic sxemalar (request/response)
│       ├── utils/          # Yordamchi funksiyalar (JWT, hash)
│       ├── core/           # Konfiguratsiya
│       └── db/             # DB session
└── frontend/                # (hali qo'shilmagan)
```

## Ishga tushirish (backend)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

copy .env.example .env      # va qiymatlarni to'ldiring
```

PostgreSQL'da `.env`dagi `DATABASE_NAME` bilan mos baza yarating, so'ng serverni ishga tushiring:

```bash
uvicorn app.main:app --reload
```

Server ishga tushgach, jadvallar avtomatik yaratiladi va API hujjatlari `http://localhost:8000/docs` manzilida ochiladi.
