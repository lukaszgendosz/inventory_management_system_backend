from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.schemes import LocationCreateScheme, LocationResponseScheme, LocationUpdateScheme
from app.services import LocationService
from app.configs.containers import Application
from app.utils.dependencies import manager_role_checker, admin_role_checker

router = APIRouter(tags=['Locations'])

@router.get('/locations')
@inject
def get_locations(
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _ = Depends(manager_role_checker)
    ) -> list[LocationResponseScheme]:
    return location_service.get_locations()

@router.get('/locations/{location_id}')
@inject
def get_locations(
    location_id: int,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _ = Depends(manager_role_checker)
    ) -> LocationResponseScheme:
    return location_service.get_location_by_id(location_id)


@router.post('/locations')
@inject
def create_location(
    request: LocationCreateScheme,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _ = Depends(admin_role_checker)
    ) -> LocationResponseScheme:
    return location_service.create_location(request)

@router.patch('/locations/{location_id}')
@inject
def update_location(
    location_id: int,
    request: LocationUpdateScheme,
    location_service: LocationService = Depends(Provide[Application.services.location_service]),
    _ = Depends(admin_role_checker)
    ) -> LocationResponseScheme:
    return location_service.update_location(location_id,request)