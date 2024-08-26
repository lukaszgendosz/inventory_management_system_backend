from typing import Iterator

from app.repositories.base_repository import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    
    def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()
        
    def get_by_id(self, user_id: int) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        
    def get_by_email(self, user_email: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == user_email).first()
            return user
        
    