from app.configs.exception.exception import NotFoundError
from app.repositories import ModelRepository
from app.models import Model
from app.schemes import ModelCreateScheme, ModelUpdateScheme, GenericFilterParams


class ModelService:

    def __init__(self, model_repository: ModelRepository) -> None:
        self._repository: ModelRepository = model_repository

    def get_models(self, params: GenericFilterParams) -> list[Model]:
        return self._repository.get_paginated_list(params)

    def get_model_by_id(self, model_id: int) -> Model:
        model = self._repository.get_by_id(model_id)
        if not model:
            raise NotFoundError("Model not found.")
        return model

    def create_model(self, request: ModelCreateScheme) -> Model:
        model = Model(**request.model_dump())
        return self._repository.save(model)

    def update_model(self, model_id: int, request: ModelUpdateScheme):
        model = self.get_model_by_id(model_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(model, key, value)
        return self._repository.save(model)

    def delete_model_by_id(self, model_id: int) -> None:
        model = self.get_model_by_id(model_id)
        return self._repository.delete(model)
