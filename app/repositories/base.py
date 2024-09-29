from typing import TypeVar, Generic, Callable, List, Tuple, Optional, Type, Any
from contextlib import AbstractContextManager
from math import ceil

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        model_class: Type[T],
    ) -> None:
        self.session_factory = session_factory
        self.model_class = model_class

    def save(self, obj: T) -> T:
        with self.session_factory() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_by_id(self, obj_id: int) -> Optional[T]:
        with self.session_factory() as session:
            return (
                session.query(self.model_class)
                .filter(self.model_class.id == obj_id)
                .first()
            )

    def get_paginated_list(
        self,
        page: int,
        page_size: int,
        filters: Optional[List[Any]] = None,
        order_by: Optional[List[Any]] = None,
    ) -> Tuple[List[T], int]:
        with self.session_factory() as session:
            query = session.query(self.model_class)

            if filters:
                query = query.filter(*filters)

            total_records = query.count()
            total_pages = ceil(total_records / page_size)

            if order_by:
                query = query.order_by(*order_by)

            offset = (page - 1) * page_size
            results = query.offset(offset).limit(page_size).all()

            return results, total_pages

    def delete(self, obj: T) -> bool:
        with self.session_factory() as session:
            session.delete(obj)
            session.commit()
            return True
