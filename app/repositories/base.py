from typing import TypeVar, Generic, Callable, List, Tuple, Optional, Type, Any
from contextlib import AbstractContextManager
from math import ceil

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemes import GenericFilterParams

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
            return session.query(self.model_class).filter(self.model_class.id == obj_id).first()

    def get_paginated_list(
        self,
        params: GenericFilterParams,
    ) -> Tuple[List[T], int]:
        with self.session_factory() as session:
            query = session.query(self.model_class)

            filters = self._generate_filters(params)

            if filters:
                query = query.filter(*filters)

            total_records = query.count()
            total_pages = ceil(total_records / params.page_size)

            if params.order_by:
                query = query.order_by(*params.order_by)

            offset = (params.page - 1) * params.page_size
            results = query.offset(offset).limit(params.page_size).all()

            return results, total_pages

    def delete(self, obj: T) -> bool:
        with self.session_factory() as session:
            session.delete(obj)
            session.commit()
            return True

    def _generate_filters(self, params: GenericFilterParams) -> Optional[List[Any]]:
        filters = []
        if params.search:
            filters.append(func.lower(self.model_class.name).contains(func.lower(params.search)))
        return filters
