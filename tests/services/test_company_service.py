import pytest
from unittest.mock import Mock, MagicMock

from app.services.company import CompanyService
from app.models import Company
from app.schemes import CompanyCreateScheme, CompanyUpdateScheme, GenericFilterParams
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def company_repository():
    return Mock()


@pytest.fixture
def company_service(company_repository):
    return CompanyService(company_repository)


@pytest.fixture
def sample_company():
    return Company(
        id=1,
        name="Test Company",
    )


class TestCompanyService:
    def test_get_companies(self, company_service, company_repository, sample_company):
        params = GenericFilterParams(page=1, page_size=10)
        company_repository.get_paginated_list.return_value = ([sample_company], 1)

        result = company_service.get_companies(params)

        assert result == ([sample_company], 1)
        company_repository.get_paginated_list.assert_called_once_with(params=params)

    def test_get_company_by_id_success(self, company_service, company_repository, sample_company):
        company_repository.get_by_id.return_value = sample_company

        result = company_service.get_company_by_id(1)

        assert result == sample_company
        company_repository.get_by_id.assert_called_once_with(1)

    def test_get_company_by_id_not_found(self, company_service, company_repository):
        company_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Company not found."):
            company_service.get_company_by_id(1)

    def test_create_company(self, company_service, company_repository, sample_company):
        company_repository.save.return_value = sample_company
        create_request = CompanyCreateScheme(name="Test Company")

        result = company_service.create_company(create_request)

        assert result == sample_company
        company_repository.save.assert_called_once()

    def test_update_company(self, company_service, company_repository, sample_company):
        company_repository.get_by_id.return_value = sample_company
        company_repository.save.return_value = sample_company
        update_request = CompanyUpdateScheme(name="Updated Company")

        result = company_service.update_company(1, update_request)

        assert result == sample_company
        company_repository.save.assert_called_once()

    def test_delete_company_success(self, company_service, company_repository, sample_company):
        sample_company.assets = []
        sample_company.users = []
        company_repository.get_by_id.return_value = sample_company

        company_service.delete_company_by_id(1)

        company_repository.delete.assert_called_once_with(sample_company)

    def test_delete_company_with_assets(self, company_service, company_repository, sample_company):
        sample_company.assets = [MagicMock()]
        company_repository.get_by_id.return_value = sample_company

        with pytest.raises(CannotDelete, match="Cannot delete company with assets assigned."):
            company_service.delete_company_by_id(1)

    def test_delete_company_with_users(self, company_service, company_repository, sample_company):
        sample_company.assets = []
        sample_company.users = [MagicMock()]
        company_repository.get_by_id.return_value = sample_company

        with pytest.raises(CannotDelete, match="Cannot delete company with users assigned."):
            company_service.delete_company_by_id(1)
