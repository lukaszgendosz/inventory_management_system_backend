from fastapi import APIRouter
from .users import router as users_router
from .assets import router as assets_router
from .departments import router as departments_router
from .locations import router as locations_router
from .companies import router as companies_router
from .manufacturers import router as manufacturers_router
from .models import router as models_router
from .suppliers import router as suppliers_router
from .asset_logs import router as asset_logs_router

routers = (
    users_router,
    assets_router,
    departments_router,
    locations_router,
    companies_router,
    manufacturers_router,
    models_router,
    suppliers_router,
    asset_logs_router,
)

router = APIRouter(prefix="/v1")
for rtr in routers:
    router.include_router(rtr)
