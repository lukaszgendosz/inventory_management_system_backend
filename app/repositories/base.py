from typing import TypeVar, Generic, Callable, List, Tuple, Optional, Type, Any
from contextlib import AbstractContextManager
from math import ceil

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session, joinedload

from app.schemes import GenericFilterParams, SortOrder

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
                attributes = params.order_by.split(".")
                column = self._resolve_order_by(attributes)

                if params.sort_order == SortOrder.DESC:
                    order_clause = desc(column)
                else:
                    order_clause = asc(column)
                query = query.order_by(order_clause)

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

    def _resolve_order_by(self, order):
        if isinstance(order, list):
            attr = self.model_class
            for part in order:
                attr = getattr(attr, part)
                if attr is None:
                    raise AttributeError(
                        f"Model '{self.model_class.__name__}' has no attribute '{part}' in order_by."
                    )
            return attr
        else:
            raise ValueError(f"Invalid order_by format.")
