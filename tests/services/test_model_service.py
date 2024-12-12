import pytest
from unittest.mock import Mock, MagicMock

from app.services.model import ModelService
from app.models import Model
from app.schemes import ModelCreateScheme, ModelUpdateScheme, GenericFilterParams
from app.configs.exception.exception import NotFoundError, CannotDelete


@pytest.fixture
def model_repository():
    return Mock()


@pytest.fixture
def model_service(model_repository):
    return ModelService(model_repository)


@pytest.fixture
def sample_model():
    return Model(
        id=1,
        name="Test Model",
        model_number="M123",
        notes="Test notes",
        manufacturer_id=1,
    )


class TestModelService:
    def test_get_models(self, model_service, model_repository, sample_model):
        params = GenericFilterParams(page=1, page_size=10)
        model_repository.get_paginated_list.return_value = ([sample_model], 1)

        result = model_service.get_models(params)

        assert result == ([sample_model], 1)
        model_repository.get_paginated_list.assert_called_once_with(params)

    def test_get_model_by_id_success(self, model_service, model_repository, sample_model):
        model_repository.get_by_id.return_value = sample_model

        result = model_service.get_model_by_id(1)

        assert result == sample_model
        model_repository.get_by_id.assert_called_once_with(1)

    def test_get_model_by_id_not_found(self, model_service, model_repository):
        model_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError, match="Model not found."):
            model_service.get_model_by_id(1)

    def test_create_model(self, model_service, model_repository, sample_model):
        model_repository.save.return_value = sample_model
        create_request = ModelCreateScheme(
            name="Test Model",
            model_number="M123",
            notes="Test notes",
            manufacturer_id=1,
        )

        result = model_service.create_model(create_request)

        assert result == sample_model
        model_repository.save.assert_called_once()

    def test_update_model(self, model_service, model_repository, sample_model):
        model_repository.get_by_id.return_value = sample_model
        model_repository.save.return_value = sample_model
        update_request = ModelUpdateScheme(name="Updated Model")

        result = model_service.update_model(1, update_request)

        assert result == sample_model
        model_repository.save.assert_called_once()

    def test_delete_model_success(self, model_service, model_repository, sample_model):
        sample_model.assets = []
        model_repository.get_by_id.return_value = sample_model

        model_service.delete_model_by_id(1)

        model_repository.delete.assert_called_once_with(sample_model)

    def test_delete_model_with_assets(self, model_service, model_repository, sample_model):
        sample_model.assets = [MagicMock()]
        model_repository.get_by_id.return_value = sample_model

        with pytest.raises(CannotDelete, match="Cannot delete model with assets assigned."):
            model_service.delete_model_by_id(1)
