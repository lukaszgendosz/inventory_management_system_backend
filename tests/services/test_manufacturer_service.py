import pytest
from unittest.mock import Mock, MagicMock

from app.services.manufacturer import ManufacturerService
from app.models import Manufacturer
from app.schemes import (
    ManufacturerCreateScheme,
    ManufacturerUpdateScheme,
    ManufacturerParamsScheme,
)
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def manufacturer_repository():
    return Mock()


@pytest.fixture
def manufacturer_service(manufacturer_repository):
    return ManufacturerService(manufacturer_repository)


@pytest.fixture
def sample_manufacturer():
    return Manufacturer(
        id=1,
        name="Test Manufacturer",
        support_url="https://test.com",
        support_phone="123456789",
        support_email="support@test.com",
    )


class TestManufacturerService:
    def test_get_manufacturers(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        params = ManufacturerParamsScheme(page=1, page_size=10)
        manufacturer_repository.get_paginated_list.return_value = ([sample_manufacturer], 1)

        result = manufacturer_service.get_manufacturers(params)

        assert result == ([sample_manufacturer], 1)
        manufacturer_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_manufacturer_by_id_success(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        manufacturer_repository.get_by_id.return_value = sample_manufacturer

        result = manufacturer_service.get_manufacturer_by_id(1)

        assert result == sample_manufacturer
        manufacturer_repository.get_by_id.assert_called_once_with(1)

    def test_get_manufacturer_by_id_not_found(self, manufacturer_service, manufacturer_repository):
        manufacturer_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Manufacturer not found."):
            manufacturer_service.get_manufacturer_by_id(1)

    def test_create_manufacturer(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        manufacturer_repository.save.return_value = sample_manufacturer
        create_request = ManufacturerCreateScheme(
            name="Test Manufacturer",
            support_url="https://test.com",
            support_phone="123456789",
            support_email="support@test.com",
        )

        result = manufacturer_service.create_manufacturer(create_request)

        assert result == sample_manufacturer
        manufacturer_repository.save.assert_called_once()

    def test_update_manufacturer(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        manufacturer_repository.get_by_id.return_value = sample_manufacturer
        manufacturer_repository.save.return_value = sample_manufacturer
        update_request = ManufacturerUpdateScheme(name="Updated Manufacturer")

        result = manufacturer_service.update_manufacturer(1, update_request)

        assert result == sample_manufacturer
        manufacturer_repository.save.assert_called_once()

    def test_delete_manufacturer_success(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        sample_manufacturer.models = []
        manufacturer_repository.get_by_id.return_value = sample_manufacturer

        manufacturer_service.delete_manufacturer_by_id(1)

        manufacturer_repository.delete.assert_called_once_with(sample_manufacturer)

    def test_delete_manufacturer_with_models(
        self, manufacturer_service, manufacturer_repository, sample_manufacturer
    ):
        sample_manufacturer.models = [MagicMock()]
        manufacturer_repository.get_by_id.return_value = sample_manufacturer

        with pytest.raises(CannotDelete, match="Cannot delete manufacturer with models assigned."):
            manufacturer_service.delete_manufacturer_by_id(1)
