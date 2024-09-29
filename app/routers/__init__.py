from fastapi import APIRouter
from app.routers.v1 import router as v1_router
from .auth import router as auth_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)
router.include_router(auth_router)
