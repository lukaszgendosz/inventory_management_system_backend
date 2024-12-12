import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import datetime

from app.repositories.user import UserRepository
from app.models import User
from app.schemes import UserParamsScheme, Role


class TestUserRepository:
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
    def sample_user(self):
        return User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="hashed_password",
            role=Role.USER,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    @pytest.fixture
    def repository(self, session_factory):
        return UserRepository(session_factory, User)

    def test_get_by_email(self, repository, session, sample_user):
        query = session.query.return_value
        query.filter.return_value.first.return_value = sample_user
        session.__enter__.return_value.query.return_value = query

        result = repository.get_by_email("test@example.com")

        assert result == sample_user
        session.query.assert_called_once_with(User)

    def test_generate_filters(self, repository):
        params = UserParamsScheme(
            page=1,
            page_size=10,
            search="test",
            is_active=[True],
            company_id=[1],
            location_id=[1],
            role=[Role.USER],
        )

        filters = repository._generate_filters(params)

        assert len(filters) == 5
