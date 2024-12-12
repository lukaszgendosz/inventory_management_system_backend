import pytest
from unittest.mock import Mock, patch
from datetime import timedelta

from app.services.auth import AuthService
from app.schemes import UserLoginScheme, TokenResponseScheme, Role
from app.configs.exception.exception import AuthenticationError
from app.models import User


@pytest.fixture
def user_service():
    return Mock()


@pytest.fixture
def auth_service(user_service):
    return AuthService(user_service)


@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        password="hashed_password",
        first_name="Test",
        last_name="User",
        role=Role.USER,
        is_active=True,
    )


class TestAuthService:
    def test_login_success(self, auth_service, user_service, sample_user):
        user_service.get_user_by_email.return_value = sample_user
        credentials = UserLoginScheme(email="test@example.com", password="Password123!")

        with patch("app.services.auth.verify_password", return_value=True), patch(
            "app.services.auth.create_token"
        ) as mock_create_token:
            mock_create_token.side_effect = ["access_token", "refresh_token"]
            result = auth_service.login(credentials)

        assert isinstance(result, TokenResponseScheme)
        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"

        mock_create_token.assert_any_call({"user": {"id": sample_user.id}})
        mock_create_token.assert_any_call(
            {"user": {"id": sample_user.id}},
            expires_delta=timedelta(days=14),
            is_refresh=True,
        )

    def test_login_invalid_credentials(self, auth_service, user_service, sample_user):
        user_service.get_user_by_email.return_value = sample_user
        credentials = UserLoginScheme(email="test@example.com", password="WrongPassword")

        with patch("app.services.auth.verify_password", return_value=False):
            with pytest.raises(AuthenticationError, match="Incorrect email address or password."):
                auth_service.login(credentials)

    def test_login_user_not_found(self, auth_service, user_service):
        user_service.get_user_by_email.return_value = None
        credentials = UserLoginScheme(email="nonexistent@example.com", password="Password123!")

        with pytest.raises(AuthenticationError, match="Incorrect email address or password."):
            auth_service.login(credentials)

    def test_login_inactive_user(self, auth_service, user_service, sample_user):
        sample_user.is_active = False
        user_service.get_user_by_email.return_value = sample_user
        credentials = UserLoginScheme(email="test@example.com", password="Password123!")

        with patch("app.services.auth.verify_password", return_value=True):
            with pytest.raises(
                AuthenticationError,
                match="Your account is not active. Please contact your administrator.",
            ):
                auth_service.login(credentials)

    def test_refresh_token_success(self, auth_service, user_service, sample_user):
        user_service.get_user_by_id.return_value = sample_user
        token_data = {"user": {"id": 1}}

        with patch("app.services.auth.create_token", return_value="new_access_token"):
            result = auth_service.refresh_token(token_data)

        assert isinstance(result, TokenResponseScheme)
        assert result.access_token == "new_access_token"
        assert result.refresh_token == ""

        user_service.get_user_by_id.assert_called_once_with(1)
