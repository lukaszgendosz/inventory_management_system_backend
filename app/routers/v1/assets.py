from typing import Annotated

from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    AssetCreateScheme,
    AssetResponseScheme,
    AssetUpdateScheme,
    AssetPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import AssetService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Assets"])


@router.get("/assets")
@inject
def get_assets(
    filter_query: Annotated[GenericFilterParams, Query()],
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    _=Depends(manager_role_checker),
) -> AssetPaginatedResponseScheme:
    assets, total_pages = asset_service.get_assets(params=filter_query)
    assets_schemas = [AssetResponseScheme.model_validate(asset) for asset in assets]
    return AssetPaginatedResponseScheme(total_pages=total_pages, data=assets_schemas)


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
    _=Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.create_asset(request)


@router.patch("/assets/{asset_id}")
@inject
def update_asset(
    asset_id: int,
    request: AssetUpdateScheme,
    asset_service: AssetService = Depends(Provide[Application.services.asset_service]),
    _=Depends(manager_role_checker),
) -> AssetResponseScheme:
    return asset_service.update_asset(asset_id, request)
