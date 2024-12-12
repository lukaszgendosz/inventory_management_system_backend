import pytest
from unittest.mock import Mock, MagicMock

from app.services.location import LocationService
from app.models import Location
from app.schemes import LocationCreateScheme, LocationUpdateScheme, GenericFilterParams
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def location_repository():
    return Mock()


@pytest.fixture
def location_service(location_repository):
    return LocationService(location_repository)


@pytest.fixture
def sample_location():
    return Location(
        id=1,
        name="Test Location",
    )


class TestLocationService:
    def test_get_locations(self, location_service, location_repository, sample_location):
        params = GenericFilterParams(page=1, page_size=10)
        location_repository.get_paginated_list.return_value = ([sample_location], 1)

        result = location_service.get_locations(params)

        assert result == ([sample_location], 1)
        location_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_location_by_id_success(
        self, location_service, location_repository, sample_location
    ):
        location_repository.get_by_id.return_value = sample_location

        result = location_service.get_location_by_id(1)

        assert result == sample_location
        location_repository.get_by_id.assert_called_once_with(1)

    def test_get_location_by_id_not_found(self, location_service, location_repository):
        location_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Location not found."):
            location_service.get_location_by_id(1)

    def test_create_location(self, location_service, location_repository, sample_location):
        location_repository.save.return_value = sample_location
        create_request = LocationCreateScheme(name="Test Location")

        result = location_service.create_location(create_request)

        assert result == sample_location
        location_repository.save.assert_called_once()

    def test_update_location(self, location_service, location_repository, sample_location):
        location_repository.get_by_id.return_value = sample_location
        location_repository.save.return_value = sample_location
        update_request = LocationUpdateScheme(name="Updated Location")

        result = location_service.update_location(1, update_request)

        assert result == sample_location
        location_repository.save.assert_called_once()

    def test_delete_location_success(self, location_service, location_repository, sample_location):
        sample_location.assets = []
        sample_location.users = []
        location_repository.get_by_id.return_value = sample_location

        location_service.delete_location_by_id(1)

        location_repository.delete.assert_called_once_with(sample_location)

    def test_delete_location_with_assets(
        self, location_service, location_repository, sample_location
    ):
        sample_location.assets = [MagicMock()]
        sample_location.users = []
        location_repository.get_by_id.return_value = sample_location

        with pytest.raises(CannotDelete, match="Cannot delete location with assets assigned."):
            location_service.delete_location_by_id(1)

    def test_delete_location_with_users(
        self, location_service, location_repository, sample_location
    ):
        sample_location.assets = []
        sample_location.users = [MagicMock()]
        location_repository.get_by_id.return_value = sample_location

        with pytest.raises(CannotDelete, match="Cannot delete location with users assigned."):
            location_service.delete_location_by_id(1)
