from fastapi import APIRouter
from .users import router as users_router
from .assets import router as assets_router
from .departments import router as departments_router

routers = (users_router,
           assets_router,
           departments_router)

router = APIRouter(prefix='/v1')
for rtr in routers:
    router.include_router(rtr)
router.include_router(users_router)
