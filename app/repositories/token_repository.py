from typing import Iterator 

from app.repositories.base_repository import BaseRepository
from app.models import Token

class TokenRepository(BaseRepository):
    
    def get_all_user_tokens(self, user_id) -> Iterator[Token]:
        with self.session_factory() as session:
            return session.query(Token).filter(Token.user_id == user_id).all()
        
    def get_by_id(self, token_id: int) -> Token:
        with self.session_factory() as session:
            user = session.query(Token).filter(Token.id == token_id).first()
            return user
    

        
    