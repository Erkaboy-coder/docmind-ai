from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router


router = APIRouter()

router.include_router(health_router, tags=["Health"])
router.include_router(users_router,tags=["Users"])
router.include_router(auth_router, tags=["Auth"])
router.include_router(documents_router, tags=["Documents"])