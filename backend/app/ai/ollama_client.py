import requests

from app.core.config import settings

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = (
    "Siz hujjatlar bo'yicha savol-javob yordamchisiz. Qat'iy qoidalar:\n"
    "1. Faqat pastda berilgan \"Kontekst\" bo'limidagi ma'lumotga asoslanib javob bering.\n"
    "2. Agar javob kontekstda aniq bo'lmasa, \"Bu ma'lumot hujjatda topilmadi\" deb ayting "
    "— hech qachon o'zingizdan to'qib chiqarmang.\n"
    "3. Raqam, sana, telefon, email kabi aniq faktlarni kontekstdan so'zma-so'z, "
    "o'zgartirmasdan ko'chiring.\n"
    "4. Javobni qisqa va aniq bering — ortiqcha sharh, tavsiya yoki umumiy gaplar "
    "qo'shmang, faqat savolga javob bering.\n"
    "5. O'zbek tilida javob bering."
)


def ask_llm(question: str, context: str) -> str:
    prompt = f"Kontekst:\n{context}\n\nSavol: {question}"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": settings.ollama_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.2
            },
        },
        timeout=180,
    )
    response.raise_for_status()

    return response.json()["message"]["content"]
