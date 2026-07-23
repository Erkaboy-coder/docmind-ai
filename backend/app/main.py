from fastapi import FastAPI

from app.api.router import router
from app.db.session import Base, engine

import app.models

app = FastAPI(
    title="DocMind AI",
    description="AI-powered Document Assistant",
    version="0.1.0"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to DocMind AI 🚀"
    }