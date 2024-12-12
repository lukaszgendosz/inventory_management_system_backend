import pytest
from unittest.mock import Mock, MagicMock

from app.services.department import DepartmentService
from app.models import Department
from app.schemes import DepartmentCreateScheme, DepartmentUpdateScheme, GenericFilterParams
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def department_repository():
    return Mock()


@pytest.fixture
def department_service(department_repository):
    return DepartmentService(department_repository)


@pytest.fixture
def sample_department():
    return Department(
        id=1,
        name="Test Department",
    )


class TestDepartmentService:
    def test_get_departments(self, department_service, department_repository, sample_department):
        params = GenericFilterParams(page=1, page_size=10)
        department_repository.get_paginated_list.return_value = ([sample_department], 1)

        result = department_service.get_departments(params)

        assert result == ([sample_department], 1)
        department_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_department_by_id_success(
        self, department_service, department_repository, sample_department
    ):
        department_repository.get_by_id.return_value = sample_department

        result = department_service.get_department_by_id(1)

        assert result == sample_department
        department_repository.get_by_id.assert_called_once_with(1)

    def test_get_department_by_id_not_found(self, department_service, department_repository):
        department_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Department not found."):
            department_service.get_department_by_id(1)

    def test_create_department(self, department_service, department_repository, sample_department):
        department_repository.save.return_value = sample_department
        create_request = DepartmentCreateScheme(name="Test Department")

        result = department_service.create_department(create_request)

        assert result == sample_department
        department_repository.save.assert_called_once()

    def test_update_department(self, department_service, department_repository, sample_department):
        department_repository.get_by_id.return_value = sample_department
        department_repository.save.return_value = sample_department
        update_request = DepartmentUpdateScheme(name="Updated Department")

        result = department_service.update_department(1, update_request)

        assert result == sample_department
        department_repository.save.assert_called_once()

    def test_delete_department_success(
        self, department_service, department_repository, sample_department
    ):
        sample_department.users = []
        department_repository.get_by_id.return_value = sample_department

        department_service.delete_department_by_id(1)

        department_repository.delete.assert_called_once_with(sample_department)

    def test_delete_department_with_users(
        self, department_service, department_repository, sample_department
    ):
        sample_department.users = [MagicMock()]
        department_repository.get_by_id.return_value = sample_department

        with pytest.raises(CannotDelete, match="Cannot delete department with users assigned."):
            department_service.delete_department_by_id(1)
