from app.repositories.base import BaseRepository
from app.models import AssetLogs


class AssetLogsRepository(BaseRepository[AssetLogs]):

    def get_by_asset_id(self, asset_id: int) -> list[AssetLogs]:
        with self.session_factory() as session:
            return (
                session.query(self.model_class)
                .filter(self.model_class.asset_id == asset_id)
                .order_by(self.model_class.created_at.desc())
                .all()
            )
