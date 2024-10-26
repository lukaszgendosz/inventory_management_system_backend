from app.configs.exception.exception import NotFoundError, AlreadyExistsError
from app.repositories import AssetRepository
from app.models import Asset
from app.schemes import AssetCreateScheme, AssetUpdateScheme, GenericFilterParams


class AssetService:

    def __init__(self, asset_repository: AssetRepository) -> None:
        self._repository: AssetRepository = asset_repository

    def get_assets(self, params: GenericFilterParams) -> list[Asset]:
        return self._repository.get_paginated_list(params)

    def get_asset_by_id(self, asset_id: int) -> Asset:
        asset = self._repository.get_by_id(asset_id)
        if not asset:
            raise NotFoundError("asset not found.")
        return asset

    def create_asset(self, request: AssetCreateScheme) -> Asset:
        # asset = self.get_asset_by_serial(request.serial_number)
        # if asset:
        #     raise AlreadyExistsError('asset already exists.')
        asset = Asset(**request.model_dump())
        asset = self._repository.save(asset)
        return asset

    def update_asset(self, asset_id: int, request: AssetUpdateScheme) -> Asset:
        asset = self.get_asset_by_id(asset_id)

        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(asset, key, value)
        return self._repository.save(asset)
