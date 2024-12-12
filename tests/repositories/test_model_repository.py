import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.repositories.model import ModelRepository
from app.models import Model
from app.schemes import ModelParamsScheme


class TestModelRepository:
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
        return ModelRepository(session_factory, Model)

    @pytest.fixture
    def sample_model(self):
        return Model(
            id=1,
            name="Test Model",
            model_number="M123",
            notes="Test notes",
            manufacturer_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def test_generate_filters(self, repository):
        params = ModelParamsScheme(
            page=1,
            page_size=10,
            search="test",
            manufacturer_id=[1],
        )

        filters = repository._generate_filters(params)

        assert len(filters) == 2  # search + manufacturer_id
