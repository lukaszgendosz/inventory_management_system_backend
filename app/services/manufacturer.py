from app.configs.exception.exception import NotFoundError
from app.repositories import ManufacturerRepository
from app.models import Manufacturer
from app.schemes import ManufacturerCreateScheme, ManufacturerUpdateScheme
from app.schemes.generic_params import GenericFilterParams


class ManufacturerService:

    def __init__(self, manufacturer_repository: ManufacturerRepository) -> None:
        self._repository: ManufacturerRepository = manufacturer_repository

    def get_manufacturers(self, params: GenericFilterParams) -> list[Manufacturer]:
        return self._repository.get_paginated_list(params)

    def get_manufacturer_by_id(self, manufacturer_id: int) -> Manufacturer:
        manufacturer = self._repository.get_by_id(manufacturer_id)
        if not manufacturer:
            raise NotFoundError("Manufacturer not found.")
        return manufacturer

    def create_manufacturer(self, request: ManufacturerCreateScheme) -> Manufacturer:
        manufacturer = Manufacturer(**request.model_dump())
        return self._repository.save(manufacturer)

    def update_manufacturer(self, manufacturer_id: int, request: ManufacturerUpdateScheme):
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(manufacturer, key, value)
        return self._repository.save(manufacturer)

    def delete_manufacturer_by_id(self, manufacturer_id: int) -> None:
        manufacturer = self.get_manufacturer_by_id(manufacturer_id)
        return self._repository.delete(manufacturer)
