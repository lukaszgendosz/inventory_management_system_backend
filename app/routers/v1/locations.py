from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response
from dependency_injector.wiring import inject, Provide

from app.schemes import (
    LocationCreateScheme,
    LocationResponseScheme,
    LocationUpdateScheme,
    LocationPaginatedResponseScheme,
    GenericFilterParams,
)
from app.services import LocationService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=["Locations"])


@router.get("/locations")
@inject
def get_locations(
    filter_query: Annotated[GenericFilterParams, Query()],
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _=Depends(manager_role_checker),
) -> LocationPaginatedResponseScheme:
    locations, total_pages = location_service.get_locations(params=filter_query)
    locations_schmeas = [LocationResponseScheme.model_validate(location) for location in locations]
    return LocationPaginatedResponseScheme(total_pages=total_pages, data=locations_schmeas)


@router.get("/locations/{location_id}")
@inject
def get_locations(
    location_id: int,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _=Depends(manager_role_checker),
) -> LocationResponseScheme:
    return location_service.get_location_by_id(location_id)


@router.post("/locations")
@inject
def create_location(
    request: LocationCreateScheme,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _=Depends(admin_role_checker),
) -> LocationResponseScheme:
    return location_service.create_location(request)


@router.patch("/locations/{location_id}")
@inject
def update_location(
    location_id: int,
    request: LocationUpdateScheme,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _=Depends(admin_role_checker),
) -> LocationResponseScheme:
    return location_service.update_location(location_id, request)


@router.delete("/locations/{location_id}")
@inject
def update_location(
    location_id: int,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _=Depends(admin_role_checker),
):
    location_service.delete_location_by_id(location_id)
    return Response("OK", status_code=200)
