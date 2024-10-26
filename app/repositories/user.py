from typing import Optional, List, Any

from sqlalchemy import func

from app.repositories.base import BaseRepository
from app.models.user import User
from app.schemes import GenericFilterParams


class UserRepository(BaseRepository[User]):
    def get_by_email(self, user_email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return user

    def _generate_filters(self, params: GenericFilterParams) -> Optional[List[Any]]:
        filters = []
        if params.search:
            filters.append(
                (
                    func.lower(self.model_class.first_name).contains(func.lower(params.search))
                    | func.lower(self.model_class.last_name).contains(func.lower(params.search))
                    | func.lower(self.model_class.email).contains(func.lower(params.search))
                )
            )
        return filters
