from typing import Any, List
from app.repositories.base import BaseRepository
from app.models import Model
from app.schemes import ModelParamsScheme


class ModelRepository(BaseRepository[Model]):

    def _generate_filters(self, params: ModelParamsScheme) -> List[Any]:
        filters = super()._generate_filters(params)
        if params.manufacturer_id:
            filters.append(self.model_class.manufacturer_id.in_(params.manufacturer_id))
        return filters
