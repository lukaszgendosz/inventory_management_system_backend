from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import AssetLogsResponseScheme
from app.services import AssetLogsService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker

router = APIRouter(tags=["Asset logs"])


@router.get("/asset-logs")
@inject
def get_asset(
    asset_id: int,
    asset_logs_service: AssetLogsService = Depends(
        Provide[Application.services.asset_logs_service]
    ),
    _=Depends(manager_role_checker),
) -> list[AssetLogsResponseScheme]:
    return asset_logs_service.get_logs_by_asset_id(asset_id)
