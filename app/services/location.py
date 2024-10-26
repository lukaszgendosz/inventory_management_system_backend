from app.configs.exception.exception import NotFoundError
from app.repositories import LocationRepository
from app.models import Location
from app.schemes import LocationCreateScheme, LocationUpdateScheme, GenericFilterParams


class LocationService:

    def __init__(self, location_repository: LocationRepository) -> None:
        self._repository: LocationRepository = location_repository

    def get_locations(self, params: GenericFilterParams) -> list[Location]:
        return self._repository.get_paginated_list(params)

    def get_location_by_id(self, location_id: int) -> Location:
        location = self._repository.get_by_id(location_id)
        if not location:
            raise NotFoundError("Location not found.")
        return location

    def create_location(self, request: LocationCreateScheme) -> Location:
        location = Location(**request.model_dump())
        return self._repository.save(location)

    def update_location(self, location_id: int, request: LocationUpdateScheme):
        location = self.get_location_by_id(location_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(location, key, value)
        return self._repository.save(location)

    def delete_location_by_id(self, location_id: int) -> None:
        location = self.get_location_by_id(location_id)
        return self._repository.delete(location)
