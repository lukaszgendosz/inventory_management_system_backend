import pytest
from unittest.mock import Mock, patch

from app.models.user import User
from app.services.user import UserService
from app.schemes import UserCreateScheme, UserUpdateScheme, GenericFilterParams, Role
from app.configs.exception.exception import NotFoundError, AlreadyExistsError, AccessDeniedError


@pytest.fixture
def user_repository():
    return Mock()


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="hashed_password",
        role=Role.USER,
        is_active=True,
    )


class TestUserService:
    def test_get_users(self, user_service, user_repository, sample_user):
        params = GenericFilterParams(page=1, per_page=10)
        user_repository.get_paginated_list.return_value = ([sample_user], 1)

        result = user_service.get_users(params)

        assert result == ([sample_user], 1)
        user_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_user_by_id_success(self, user_service, user_repository, sample_user):
        user_repository.get_by_id.return_value = sample_user

        result = user_service.get_user_by_id(1)

        assert result == sample_user
        user_repository.get_by_id.assert_called_once_with(1)

    def test_get_user_by_id_not_found(self, user_service, user_repository):
        user_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="User not found."):
            user_service.get_user_by_id(1)

    def test_get_user_by_email(self, user_service, user_repository, sample_user):
        user_repository.get_by_email.return_value = sample_user

        result = user_service.get_user_by_email("test@example.com")

        assert result == sample_user
        user_repository.get_by_email.assert_called_once_with("test@example.com")

    @patch("app.services.user.hash_password")
    def test_create_user_success(
        self, mock_hash_password, user_service, user_repository, sample_user
    ):
        user_repository.get_by_email.return_value = None
        user_repository.save.return_value = sample_user
        mock_hash_password.return_value = "hashed_password"

        create_request = UserCreateScheme(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="Password123!",
            role=Role.USER,
        )

        result = user_service.create_user(create_request)

        assert result == sample_user
        mock_hash_password.assert_called_once_with("Password123!")
        user_repository.save.assert_called_once()

    def test_create_user_already_exists(self, user_service, user_repository, sample_user):
        user_repository.get_by_email.return_value = sample_user

        create_request = UserCreateScheme(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="Password123!",
            role=Role.USER,
        )

        with pytest.raises(AlreadyExistsError, match="User already exists."):
            user_service.create_user(create_request)

    def test_update_user_success(self, user_service, user_repository, sample_user):
        user_repository.get_by_id.return_value = sample_user
        user_repository.save.return_value = sample_user

        update_request = UserUpdateScheme(first_name="Updated", last_name="Name")

        result = user_service.update_user(1, update_request)

        assert result == sample_user
        user_repository.save.assert_called_once()

    def test_deactivate_user_success(self, user_service, user_repository, sample_user):
        user_repository.get_by_id.return_value = sample_user
        current_user = User(id=2, email="admin@example.com", first_name="Admin", last_name="User")

        user_service.deactivate_user(1, current_user)

        assert not sample_user.is_active
        user_repository.save.assert_called_once()

    def test_deactivate_self_not_allowed(self, user_service, user_repository, sample_user):
        user_repository.get_by_id.return_value = sample_user

        with pytest.raises(AccessDeniedError, match="You cannot deactivate yourself."):
            user_service.deactivate_user(1, sample_user)

    def test_activate_user_success(self, user_service, user_repository, sample_user):
        sample_user.is_active = False
        user_repository.get_by_id.return_value = sample_user

        user_service.activate_user(1)

        assert sample_user.is_active
        user_repository.save.assert_called_once()
