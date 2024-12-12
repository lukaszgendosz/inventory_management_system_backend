import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session, Mapped
from datetime import datetime

from app.repositories.base import BaseRepository
from app.schemes import GenericFilterParams, SortOrder
from app.models.base import Base


class SampleModel(Base):
    __tablename__ = "sample_model"
    name: Mapped[str]


class TestBaseRepository:
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
    def sample_model(self):
        return SampleModel(
            id=1,
            name="Test Model",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    @pytest.fixture
    def repository(self, session_factory):
        return BaseRepository(session_factory, SampleModel)

    def test_get_by_id(self, repository, session, sample_model):
        query = session.query.return_value
        query.filter.return_value.first.return_value = sample_model
        session.__enter__.return_value.query.return_value = query

        result = repository.get_by_id(1)

        assert result == sample_model
        session.query.assert_called_once_with(SampleModel)
        query.filter.assert_called_once()

    def test_save(self, repository, session):
        obj = Mock()

        result = repository.save(obj)

        assert result == obj
        session.add.assert_called_once_with(obj)
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(obj)

    def test_delete(self, repository, session):
        obj = Mock()

        result = repository.delete(obj)

        assert result is True
        session.delete.assert_called_once_with(obj)
        session.commit.assert_called_once()

    def test_get_paginated_list(self, repository, session, sample_model):
        params = GenericFilterParams(
            page=1, page_size=10, search="test", order_by="id", sort_order=SortOrder.ASC
        )

        query = session.query.return_value
        query.filter.return_value.count.return_value = 20
        query.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [
            sample_model
        ]
        session.__enter__.return_value.query.return_value = query

        results, total_pages = repository.get_paginated_list(params)

        assert results == [sample_model]
        assert total_pages == 2
        session.query.assert_called_once_with(SampleModel)
