from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    ManufacturerCreateScheme,
    ManufacturerResponseScheme,
    ManufacturerUpdateScheme,
    ManufacturerPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import ManufacturerService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Manufacturers"])


@router.get("/manufacturers")
@inject
def get_manufacturers(
    filter_query: Annotated[GenericFilterParams, Query()],
    manufacturer_service: ManufacturerService = Depends(
        Provide[Application.services.manufacturer_service]
    ),
    _=Depends(manager_role_checker),
) -> ManufacturerPaginatedResponseScheme:
    manufacturers, total_pages = manufacturer_service.get_manufacturers(filter_query)
    manufacturers_schmeas = [
        ManufacturerResponseScheme.model_validate(manufacturer) for manufacturer in manufacturers
    ]
    return ManufacturerPaginatedResponseScheme(total_pages=total_pages, data=manufacturers_schmeas)


@router.get("/manufacturers/{manufacturer_id}")
@inject
def get_manufacturers(
    manufacturer_id: int,
    manufacturer_service: ManufacturerService = Depends(
        Provide[Application.services.manufacturer_service]
    ),
    _=Depends(manager_role_checker),
) -> ManufacturerResponseScheme:
    return manufacturer_service.get_manufacturer_by_id(manufacturer_id)


@router.post("/manufacturers")
@inject
def create_manufacturer(
    request: ManufacturerCreateScheme,
    manufacturer_service: ManufacturerService = Depends(
        Provide[Application.services.manufacturer_service]
    ),
    _=Depends(manager_role_checker),
) -> ManufacturerResponseScheme:
    return manufacturer_service.create_manufacturer(request)


@router.patch("/manufacturers/{manufacturer_id}")
@inject
def update_manufacturer(
    manufacturer_id: int,
    request: ManufacturerUpdateScheme,
    manufacturer_service: ManufacturerService = Depends(
        Provide[Application.services.manufacturer_service]
    ),
    _=Depends(manager_role_checker),
) -> ManufacturerResponseScheme:
    return manufacturer_service.update_manufacturer(manufacturer_id, request)


@router.delete("/manufacturers/{manufacturer_id}")
@inject
def update_manufacturer(
    manufacturer_id: int,
    manufacturer_service: ManufacturerService = Depends(
        Provide[Application.services.manufacturer_service]
    ),
    _=Depends(manager_role_checker),
):
    manufacturer_service.delete_manufacturer_by_id(manufacturer_id)
    return Response("OK", status_code=200)
