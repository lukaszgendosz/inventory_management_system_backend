from typing import Annotated

from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide
from fastapi.responses import StreamingResponse

from app.models.user import User
from app.schemes import (
    AssetCreateScheme,
    AssetResponseScheme,
    AssetUpdateScheme,
    AssetPaginatedResponseScheme,
    AssetParamsScheme,
    ExportType,
)
from app.services import AssetService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, user_role_checker

router = APIRouter(tags=["Assets"])


@router.get("/assets")
@inject
def get_assets(
    filter_query: Annotated[AssetParamsScheme, Query()],
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    _=Depends(manager_role_checker),
) -> AssetPaginatedResponseScheme:
    assets, total_pages = asset_service.get_assets(params=filter_query)
    assets_schemas = [AssetResponseScheme.model_validate(asset) for asset in assets]
    return AssetPaginatedResponseScheme(total_pages=total_pages, data=assets_schemas)


@router.get("/assets/export")
@inject
def get_assets(
    filter_query: Annotated[AssetParamsScheme, Query()],
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    _=Depends(manager_role_checker),
) -> StreamingResponse:
    return asset_service.export_assets(ExportType.CSV, filter_query)


@router.get("/assets/me")
@inject
def get_current_user_asset(
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    current_user=Depends(user_role_checker),
) -> list[AssetResponseScheme]:
    return asset_service.get_assets_by_user_id(current_user.id)


@router.get("/assets/{asset_id}")
@inject
def get_asset(
    asset_id: int,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    _=Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.get_asset_by_id(asset_id)


@router.post("/assets")
@inject
def create_asset(
    request: AssetCreateScheme,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    current_user: User = Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.create_asset(request, current_user.id)


@router.patch("/assets/{asset_id}")
@inject
def update_asset(
    asset_id: int,
    request: AssetUpdateScheme,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    current_user: User = Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.update_asset(asset_id, request, current_user.id)


@router.patch("/assets/{asset_id}/checkout")
@inject
def checkout_asset(
    asset_id: int,
    user_id: int,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    current_user: User = Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.checkout_asset(asset_id, user_id, current_user.id)


@router.patch("/assets/{asset_id}/checkin")
@inject
def checkin_asset(
    asset_id: int,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    current_user: User = Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.checkin_asset(asset_id, current_user.id)
