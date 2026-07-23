from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router

import app.models  # noqa: F401 -- registers all models so relationships resolve

app = FastAPI(
    title="DocMind AI",
    description="AI-powered Document Assistant",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocMind AI 🚀"
    }