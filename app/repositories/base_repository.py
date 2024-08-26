from sqlalchemy.orm import Session
from typing import Any
from contextlib import AbstractContextManager
from typing import Callable



class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        
    def save(self, obj: Any):
        with self.session_factory() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj: Any):
        with self.session_factory() as session:
            session.delete(obj)
            session.commit()
            return True

