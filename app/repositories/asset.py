from typing import Any, List, Optional
from sqlalchemy import func
from app.repositories.base import BaseRepository
from app.models import Asset, Model
from app.schemes.asset import AssetParamsScheme


class AssetRepository(BaseRepository[Asset]):

    def get_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        with self.session_factory() as session:
            user = (
                session.query(self.model_class)
                .filter(self.model_class.serial_number == serial_number)
                .first()
            )
            return user

    def get_assets_by_user_id(self, user_id: int) -> list[Asset]:
        with self.session_factory() as session:
            assets = (
                session.query(self.model_class).filter(self.model_class.user_id == user_id).all()
            )
            return assets

    def _generate_filters(self, params: AssetParamsScheme) -> Optional[List[Any]]:
        filters = []
        if params.search:
            filters.append(
                (
                    func.lower(self.model_class.name).contains(func.lower(params.search))
                    | func.lower(self.model_class.serial_number).contains(func.lower(params.search))
                )
            )

        if params.user_id:
            filters.append(self.model_class.user_id.in_(params.user_id))
        if params.company_id:
            filters.append(self.model_class.company_id.in_(params.company_id))
        if params.location_id:
            filters.append(self.model_class.location_id.in_(params.location_id))
        if params.model_id:
            filters.append(self.model_class.model_id.in_(params.model_id))
        if params.supplier_id:
            filters.append(self.model_class.supplier_id.in_(params.supplier_id))
        if params.status:
            filters.append(self.model_class.status.in_(params.status))
        if params.manufacturer_id:
            filters.append(
                self.model_class.model.has(Model.manufacturer_id.in_(params.manufacturer_id))
            )
        return filters
