import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.repositories.asset import AssetRepository
from app.models import Asset
from app.schemes import AssetParamsScheme, Status


class TestAssetRepository:
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
        return AssetRepository(session_factory, Asset)

    @pytest.fixture
    def sample_asset(self):
        return Asset(
            id=1,
            name="Test Asset",
            serial_number="SN123",
            status=Status.AVAILABLE,
            purchase_date=datetime.now(),
            purchase_cost=100.0,
        )

    def test_get_by_serial_number(self, repository, session, sample_asset):
        query = session.query.return_value
        query.filter.return_value.first.return_value = sample_asset
        session.__enter__.return_value.query.return_value = query

        result = repository.get_by_serial_number("SN123")

        assert result == sample_asset
        session.query.assert_called_once_with(Asset)

    def test_get_assets_by_user_id(self, repository, session, sample_asset):
        query = session.query.return_value
        query.filter.return_value.all.return_value = [sample_asset]
        session.__enter__.return_value.query.return_value = query

        result = repository.get_assets_by_user_id(1)

        assert result == [sample_asset]
        session.query.assert_called_once_with(Asset)

    def test_generate_filters(self, repository):
        params = AssetParamsScheme(
            page=1,
            page_size=10,
            search="test",
            user_id=[1],
            company_id=[1],
            location_id=[1],
            model_id=[1],
            supplier_id=[1],
            status=[Status.AVAILABLE],
            manufacturer_id=[1],
        )

        filters = repository._generate_filters(params)

        assert len(filters) == 8  # All filter parameters
