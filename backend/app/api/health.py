from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "Health",
        "message": "Health is running 🚀"
    }