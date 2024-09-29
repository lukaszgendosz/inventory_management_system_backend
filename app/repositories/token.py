from typing import Iterator

from app.repositories.base import BaseRepository
from app.models import Token


class TokenRepository(BaseRepository):

    def get_all_user_tokens(self, user_id) -> Iterator[Token]:
        with self.session_factory() as session:
            return session.query(Token).filter(Token.user_id == user_id).all()
