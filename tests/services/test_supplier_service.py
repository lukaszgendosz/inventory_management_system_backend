import pytest
from unittest.mock import Mock, MagicMock

from app.services.supplier import SupplierService
from app.models import Supplier
from app.schemes import SupplierCreateScheme, SupplierUpdateScheme, GenericFilterParams
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def supplier_repository():
    return Mock()


@pytest.fixture
def supplier_service(supplier_repository):
    return SupplierService(supplier_repository)


@pytest.fixture
def sample_supplier():
    return Supplier(
        id=1,
        name="Test Supplier",
        support_url="https://test.com",
        support_phone="123456789",
        support_email="support@test.com",
    )


class TestSupplierService:
    def test_get_suppliers(self, supplier_service, supplier_repository, sample_supplier):
        params = GenericFilterParams(page=1, page_size=10)
        supplier_repository.get_paginated_list.return_value = ([sample_supplier], 1)

        result = supplier_service.get_suppliers(params)

        assert result == ([sample_supplier], 1)
        supplier_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_supplier_by_id_success(
        self, supplier_service, supplier_repository, sample_supplier
    ):
        supplier_repository.get_by_id.return_value = sample_supplier

        result = supplier_service.get_supplier_by_id(1)

        assert result == sample_supplier
        supplier_repository.get_by_id.assert_called_once_with(1)

    def test_get_supplier_by_id_not_found(self, supplier_service, supplier_repository):
        supplier_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Supplier not found."):
            supplier_service.get_supplier_by_id(1)

    def test_create_supplier(self, supplier_service, supplier_repository, sample_supplier):
        supplier_repository.save.return_value = sample_supplier
        create_request = SupplierCreateScheme(
            name="Test Supplier",
            support_url="https://test.com",
            support_phone="123456789",
            support_email="support@test.com",
        )

        result = supplier_service.create_supplier(create_request)

        assert result == sample_supplier
        supplier_repository.save.assert_called_once()

    def test_update_supplier(self, supplier_service, supplier_repository, sample_supplier):
        supplier_repository.get_by_id.return_value = sample_supplier
        supplier_repository.save.return_value = sample_supplier
        update_request = SupplierUpdateScheme(name="Updated Supplier")

        result = supplier_service.update_supplier(1, update_request)

        assert result == sample_supplier
        supplier_repository.save.assert_called_once()

    def test_delete_supplier_success(self, supplier_service, supplier_repository, sample_supplier):
        sample_supplier.assets = []
        supplier_repository.get_by_id.return_value = sample_supplier

        supplier_service.delete_supplier_by_id(1)

        supplier_repository.delete.assert_called_once_with(sample_supplier)

    def test_delete_supplier_with_assets(
        self, supplier_service, supplier_repository, sample_supplier
    ):
        sample_supplier.assets = [MagicMock()]
        supplier_repository.get_by_id.return_value = sample_supplier

        with pytest.raises(CannotDelete, match="Cannot delete supplier with assets assigned."):
            supplier_service.delete_supplier_by_id(1)
