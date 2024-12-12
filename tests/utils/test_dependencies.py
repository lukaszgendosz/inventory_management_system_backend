import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials

from app.utils.dependencies import (
    TokenBearer,
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)
from app.configs.exception.exception import (
    AccessTokenRequired,
    RefreshTokenRequired,
    AuthenticationError,
)
from app.schemes import Role
from app.models import User


class TestAccessTokenBearer:
    @pytest.fixture
    def access_token_bearer(self):
        return AccessTokenBearer()

    def test_verify_token_data_success(self, access_token_bearer):
        token_data = {"user": {"id": 1}, "is_refresh": False}
        access_token_bearer.verify_token_data(token_data)

    def test_verify_token_data_failure(self, access_token_bearer):
        token_data = {"user": {"id": 1}, "is_refresh": True}
        with pytest.raises(AccessTokenRequired):
            access_token_bearer.verify_token_data(token_data)


class TestRefreshTokenBearer:
    @pytest.fixture
    def refresh_token_bearer(self):
        return RefreshTokenBearer()

    def test_verify_token_data_success(self, refresh_token_bearer):
        token_data = {"user": {"id": 1}, "is_refresh": True}
        refresh_token_bearer.verify_token_data(token_data)

    def test_verify_token_data_failure(self, refresh_token_bearer):
        token_data = {"user": {"id": 1}, "is_refresh": False}
        with pytest.raises(RefreshTokenRequired):
            refresh_token_bearer.verify_token_data(token_data)


class TestRoleChecker:
    @pytest.fixture
    def sample_user(self):
        return User(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=Role.USER,
            is_active=True,
        )

    def test_allowed_role(self, sample_user):
        checker = RoleChecker([Role.USER, Role.ADMIN])
        result = checker(sample_user)
        assert result == sample_user

    def test_forbidden_role(self, sample_user):
        checker = RoleChecker([Role.ADMIN])
        with pytest.raises(
            AuthenticationError, match="You do not have permission to perform this action."
        ):
            checker(sample_user)
