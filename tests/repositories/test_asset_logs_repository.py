import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.repositories.asset_logs import AssetLogsRepository
from app.models import AssetLogs
from app.schemes import EventType


class TestAssetLogsRepository:
    @pytest.fixture
    def session(self):
        session = MagicMock(spec=Session)
        session.__enter__.return_value = session
        return session

    @pytest.fixture
    def session_factory(self, session):
        def _session_factory():
            return session

        return _session_factory

    @pytest.fixture
    def repository(self, session_factory):
        return AssetLogsRepository(session_factory, AssetLogs)

    @pytest.fixture
    def sample_log(self):
        return AssetLogs(
            id=1,
            event_type=EventType.CREATE,
            asset_id=1,
            user_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def test_get_by_asset_id(self, repository, session, sample_log):
        query = session.query.return_value
        query.filter.return_value.order_by.return_value.all.return_value = [sample_log]
        session.__enter__.return_value.query.return_value = query

        result = repository.get_by_asset_id(1)

        assert result == [sample_log]
        session.query.assert_called_once_with(AssetLogs)
