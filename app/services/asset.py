import io
from datetime import datetime
from typing import TYPE_CHECKING, Optional

import pandas as pd
from fastapi.responses import StreamingResponse

from app.schemes import ExportType, AssetLogsCreateScheme, EventType, Status, AssetExportScheme
from app.configs.exception.exception import InvalidAssetStatus, NotFoundError, AlreadyExistsError
from app.models import Asset

if TYPE_CHECKING:
    from app.repositories import AssetRepository
    from app.services import UserService, AssetLogsService
    from app.schemes import (
        AssetCreateScheme,
        AssetUpdateScheme,
        AssetParamsScheme,
    )


class AssetService:

    def __init__(
        self,
        asset_repository: "AssetRepository",
        user_service: "UserService",
        asset_logs_service: "AssetLogsService",
    ) -> None:
        self._repository: "AssetRepository" = asset_repository
        self._user_service: "UserService" = user_service
        self._asset_logs_service: "AssetLogsService" = asset_logs_service

    def get_assets(self, params: "AssetParamsScheme") -> list[Asset]:
        return self._repository.get_paginated_list(params)

    def get_asset_by_id(self, asset_id: int) -> Asset:
        asset = self._repository.get_by_id(asset_id)
        if not asset:
            raise NotFoundError("Asset not found.")
        return asset

    def get_asset_by_serial(self, serial_number: str) -> Optional[Asset]:
        return self._repository.get_by_serial_number(serial_number)

    def create_asset(self, request: "AssetCreateScheme", user_id: int) -> Asset:
        asset = self.get_asset_by_serial(request.serial_number)
        if asset:
            raise AlreadyExistsError("Asset already exists.")
        asset = Asset(**request.model_dump())
        asset = self._repository.save(asset)
        asset_log = AssetLogsCreateScheme(
            asset_id=asset.id, event_type=EventType.CREATE, user_id=user_id
        )
        self._asset_logs_service.create_log(asset_log)
        return asset

    def update_asset(self, asset_id: int, request: "AssetUpdateScheme", user_id: int) -> Asset:
        asset = self.get_asset_by_id(asset_id)
        updated_values = {}

        for key, value in request.model_dump(exclude_unset=True).items():
            if getattr(asset, key) == value:
                continue
            if key == "status" and value == Status.DEPLOYED:
                continue
            if key == "status" and value == Status.AVAILABLE and asset.status == Status.DEPLOYED:
                continue

            old_value = getattr(asset, key)
            new_value = value

            if isinstance(new_value, Status):
                new_value = new_value.value

            if isinstance(old_value, Status):
                old_value = old_value.value

            if isinstance(old_value, datetime):
                old_value = old_value.isoformat()

            if isinstance(new_value, datetime):
                new_value = new_value.isoformat()

            updated_values[key] = {
                "old_value": old_value,
                "new_value": new_value,
            }

            setattr(asset, key, value)

        updated_asset = self._repository.save(asset)
        if updated_values:
            asset_log = AssetLogsCreateScheme(
                asset_id=asset.id,
                user_id=user_id,
                event_type=EventType.UPDATE,
                updated_values=updated_values,
            )
            self._asset_logs_service.create_log(asset_log)
        return updated_asset

    def checkout_asset(self, asset_id: int, user_id: int, current_user_id: int) -> Asset:
        asset = self.get_asset_by_id(asset_id)
        if asset.status not in [Status.AVAILABLE, Status.RESERVERD]:
            raise InvalidAssetStatus("Invalid asset status.")
        user = self._user_service.get_user_by_id(user_id)
        asset.status = Status.DEPLOYED
        asset.user_id = user.id

        updated_asset = self._repository.save(asset)
        updated_values = {
            "user": {
                "old_value": None,
                "new_value": user.first_name + " " + user.last_name,
            }
        }
        asset_log = AssetLogsCreateScheme(
            asset_id=asset.id,
            event_type=EventType.CHECKOUT,
            user_id=current_user_id,
            updated_values=updated_values,
        )
        self._asset_logs_service.create_log(asset_log)
        return updated_asset

    def checkin_asset(self, asset_id: int, user_id: int) -> Asset:
        asset = self.get_asset_by_id(asset_id)
        if asset.status != Status.DEPLOYED:
            raise InvalidAssetStatus("Invalid asset status.")
        asset.status = Status.AVAILABLE
        updated_values = {
            "user": {
                "old_value": asset.user.first_name + " " + asset.user.last_name,
                "new_value": None,
            }
        }
        asset.user_id = None
        updated_asset = self._repository.save(asset)

        asset_log = AssetLogsCreateScheme(
            asset_id=asset.id,
            user_id=user_id,
            event_type=EventType.CHECKIN,
            updated_values=updated_values,
        )
        self._asset_logs_service.create_log(asset_log)
        return updated_asset

    def get_assets_by_user_id(self, user_id: int) -> list[Asset]:
        return self._repository.get_assets_by_user_id(user_id)

    def export_assets(self, format: ExportType, params: "AssetParamsScheme") -> list[Asset]:
        assets = self.get_assets(params)
        asset_dicts = [
            AssetExportScheme.model_validate(asset, from_attributes=True).model_dump()
            for asset in assets[0]
        ]

        def csv_export(assets: list[dict]) -> list[dict]:
            df = pd.DataFrame(assets)
            print(df)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding="utf-8")
            return StreamingResponse(iter([csv_buffer.getvalue()]), media_type="text/csv")

        match format:
            case ExportType.CSV:
                return csv_export(asset_dicts)
