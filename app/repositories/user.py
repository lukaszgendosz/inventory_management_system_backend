from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    def get_by_email(self, user_email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return user
