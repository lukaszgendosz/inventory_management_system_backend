import pytest
from unittest.mock import Mock
from datetime import datetime

from app.services.asset_logs import AssetLogsService
from app.models import AssetLogs
from app.schemes import AssetLogsCreateScheme, EventType


@pytest.fixture
def asset_logs_repository():
    return Mock()


@pytest.fixture
def asset_logs_service(asset_logs_repository):
    return AssetLogsService(asset_logs_repository)


@pytest.fixture
def sample_asset_log():
    return AssetLogs(
        id=1,
        event_type=EventType.CREATE,
        user_id=1,
        asset_id=1,
        updated_values={"name": {"old_value": "Old Name", "new_value": "New Name"}},
        created_at=datetime.now(),
    )


class TestAssetLogsService:
    def test_get_logs_by_asset_id(
        self, asset_logs_service, asset_logs_repository, sample_asset_log
    ):
        asset_logs_repository.get_by_asset_id.return_value = [sample_asset_log]

        result = asset_logs_service.get_logs_by_asset_id(1)

        assert result == [sample_asset_log]
        asset_logs_repository.get_by_asset_id.assert_called_once_with(1)

    def test_create_log(self, asset_logs_service, asset_logs_repository, sample_asset_log):
        asset_logs_repository.save.return_value = sample_asset_log

        create_request = AssetLogsCreateScheme(
            event_type=EventType.CREATE,
            user_id=1,
            asset_id=1,
            updated_values={"name": {"old_value": "Old Name", "new_value": "New Name"}},
        )

        result = asset_logs_service.create_log(create_request)

        assert result == sample_asset_log
        asset_logs_repository.save.assert_called_once()
