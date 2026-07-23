import requests

from app.core.config import settings

OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = (
    "Siz hujjatlar bo'yicha yordamchisiz. Faqat quyida berilgan kontekstga "
    "asoslanib javob bering. Agar javob kontekstda bo'lmasa, buni aniq ayting "
    "va o'zingizdan to'qib chiqarmang."
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
        },
        timeout=120,
    )
    response.raise_for_status()

    return response.json()["message"]["content"]
