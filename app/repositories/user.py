from typing import Optional, List, Any

from sqlalchemy import func

from app.repositories.base import BaseRepository
from app.models.user import User
from app.schemes import UserParamsScheme


class UserRepository(BaseRepository[User]):
    def get_by_email(self, user_email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return user

    def _generate_filters(self, params: UserParamsScheme) -> Optional[List[Any]]:
        filters = []
        if params.search:
            filters.append(
                (
                    func.lower(self.model_class.first_name).contains(func.lower(params.search))
                    | func.lower(self.model_class.last_name).contains(func.lower(params.search))
                    | func.lower(self.model_class.email).contains(func.lower(params.search))
                )
            )
        if params.is_active:
            filters.append(self.model_class.is_active.in_(params.is_active))
        if params.company_id:
            filters.append(self.model_class.company_id.in_(params.company_id))
        if params.location_id:
            filters.append(self.model_class.location_id.in_(params.location_id))
        return filters
