import sys
import os
from pathlib import Path

os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_password"
os.environ["POSTGRES_DB"] = "test_db"
os.environ["POSTGRES_SERVER"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient

from app.utils.dependencies import user_role_checker, manager_role_checker, admin_role_checker
from app.models import User
from app.schemes import Role
from app.main import app


@pytest.fixture
def mock_user_service():
    return Mock()


@pytest.fixture
def mock_auth_service():
    return Mock()


@pytest.fixture
def mock_manager_user():
    return User(
        id=1,
        email="manager@test.com",
        first_name="Test",
        last_name="Manager",
        role=Role.MANAGER,
        is_active=True,
    )


@pytest.fixture
def mock_admin_user():
    return User(
        id=2,
        email="admin@test.com",
        first_name="Test",
        last_name="Admin",
        role=Role.ADMIN,
        is_active=True,
    )


@pytest.fixture
def mock_regular_user():
    return User(
        id=3,
        email="user@test.com",
        first_name="Test",
        last_name="User",
        role=Role.USER,
        is_active=True,
    )


@pytest.fixture
def client(mock_regular_user):
    def override_regular_user():
        return mock_regular_user

    def override_manager_user():
        return mock_manager_user

    def override_admin_user():
        return mock_admin_user

    app.dependency_overrides[user_role_checker] = override_regular_user
    app.dependency_overrides[manager_role_checker] = override_manager_user
    app.dependency_overrides[admin_role_checker] = override_admin_user

    yield TestClient(app)
    app.dependency_overrides.clear()
