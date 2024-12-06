from app.repositories import AssetLogsRepository
from app.models import AssetLogs
from app.schemes import GenericFilterParams, AssetLogsCreateScheme
from app.configs.exception.exception import NotFoundError


class AssetLogsService:

    def __init__(self, asset_logs_repository: AssetLogsRepository) -> None:
        self._repository: AssetLogsRepository = asset_logs_repository

    def get_logs_by_asset_id(self, asset_id: int) -> list[AssetLogs]:
        return self._repository.get_by_asset_id(asset_id)

    def create_log(self, request: AssetLogsCreateScheme) -> AssetLogs:

        company = AssetLogs(**request.model_dump())
        return self._repository.save(company)
