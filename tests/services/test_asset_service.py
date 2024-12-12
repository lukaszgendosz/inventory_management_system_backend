import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from app.models import Asset
from app.services.asset import AssetService
from app.schemes import (
    AssetCreateScheme,
    AssetUpdateScheme,
    AssetParamsScheme,
    Status,
    EventType,
    ExportType,
)
from app.configs.exception.exception import NotFoundError, AlreadyExistsError, InvalidAssetStatus


@pytest.fixture
def asset_repository():
    return Mock()


@pytest.fixture
def user_service():
    return Mock()


@pytest.fixture
def asset_logs_service():
    return Mock()


@pytest.fixture
def asset_service(asset_repository, user_service, asset_logs_service):
    return AssetService(asset_repository, user_service, asset_logs_service)


@pytest.fixture
def sample_asset():
    return Asset(
        id=1,
        name="Test Asset",
        serial_number="SN123",
        status=Status.AVAILABLE,
        purchase_date=datetime.now(),
        purchase_cost=100.0,
    )


class TestAssetService:
    def test_get_assets(self, asset_service, asset_repository, sample_asset):
        params = AssetParamsScheme(page=1, page_size=10)
        asset_repository.get_paginated_list.return_value = ([sample_asset], 1)

        result = asset_service.get_assets(params)

        assert result == ([sample_asset], 1)
        asset_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_asset_by_id_success(self, asset_service, asset_repository, sample_asset):
        asset_repository.get_by_id.return_value = sample_asset

        result = asset_service.get_asset_by_id(1)

        assert result == sample_asset
        asset_repository.get_by_id.assert_called_once_with(1)

    def test_get_asset_by_id_not_found(self, asset_service, asset_repository):
        asset_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Asset not found."):
            asset_service.get_asset_by_id(1)

    def test_get_asset_by_serial(self, asset_service, asset_repository, sample_asset):
        asset_repository.get_by_serial_number.return_value = sample_asset

        result = asset_service.get_asset_by_serial("SN123")

        assert result == sample_asset
        asset_repository.get_by_serial_number.assert_called_once_with("SN123")

    def test_create_asset_success(
        self, asset_service, asset_repository, asset_logs_service, sample_asset
    ):
        asset_repository.get_by_serial_number.return_value = None
        asset_repository.save.return_value = sample_asset

        create_request = AssetCreateScheme(
            name="Test Asset",
            serial_number="SN123",
            status=Status.AVAILABLE,
        )

        result = asset_service.create_asset(create_request, user_id=1)

        assert result == sample_asset
        asset_repository.save.assert_called_once()
        asset_logs_service.create_log.assert_called_once()

    def test_create_asset_already_exists(self, asset_service, asset_repository, sample_asset):
        asset_repository.get_by_serial_number.return_value = sample_asset

        create_request = AssetCreateScheme(
            name="Test Asset",
            serial_number="SN123",
            status=Status.AVAILABLE,
        )

        with pytest.raises(AlreadyExistsError, match="Asset already exists."):
            asset_service.create_asset(create_request, user_id=1)

    def test_update_asset_success(
        self, asset_service, asset_repository, asset_logs_service, sample_asset
    ):
        asset_repository.get_by_id.return_value = sample_asset
        asset_repository.save.return_value = sample_asset

        update_request = AssetUpdateScheme(name="Updated Asset")

        result = asset_service.update_asset(1, update_request, user_id=1)

        assert result == sample_asset
        asset_repository.save.assert_called_once()
        asset_logs_service.create_log.assert_called_once()

    def test_checkout_asset_success(
        self, asset_service, asset_repository, user_service, asset_logs_service, sample_asset
    ):
        asset_repository.get_by_id.return_value = sample_asset
        user_service.get_user_by_id.return_value = Mock(id=1, first_name="Test", last_name="User")
        asset_repository.save.return_value = sample_asset

        result = asset_service.checkout_asset(1, user_id=1, current_user_id=2)

        assert result == sample_asset
        assert result.status == Status.DEPLOYED
        assert result.user_id == 1
        asset_logs_service.create_log.assert_called_once()

    def test_checkout_asset_invalid_status(self, asset_service, asset_repository, sample_asset):
        sample_asset.status = Status.DEPLOYED
        asset_repository.get_by_id.return_value = sample_asset

        with pytest.raises(InvalidAssetStatus, match="Invalid asset status."):
            asset_service.checkout_asset(1, user_id=1, current_user_id=2)

    def test_checkin_asset_success(
        self, asset_service, asset_repository, asset_logs_service, sample_asset
    ):
        sample_asset.status = Status.DEPLOYED
        sample_asset.user = MagicMock(first_name="Test", last_name="User")
        asset_repository.get_by_id.return_value = sample_asset
        asset_repository.save.return_value = sample_asset

        result = asset_service.checkin_asset(1, user_id=1)

        assert result == sample_asset
        assert result.status == Status.AVAILABLE
        assert result.user_id is None
        asset_logs_service.create_log.assert_called_once()

    def test_checkin_asset_invalid_status(self, asset_service, asset_repository, sample_asset):
        sample_asset.status = Status.AVAILABLE
        asset_repository.get_by_id.return_value = sample_asset

        with pytest.raises(InvalidAssetStatus, match="Invalid asset status."):
            asset_service.checkin_asset(1, user_id=1)

    def test_get_assets_by_user_id(self, asset_service, asset_repository, sample_asset):
        asset_repository.get_assets_by_user_id.return_value = [sample_asset]

        result = asset_service.get_assets_by_user_id(1)

        assert result == [sample_asset]
        asset_repository.get_assets_by_user_id.assert_called_once_with(1)
