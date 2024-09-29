from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponseScheme(BaseModel, Generic[T]):
    total_pages: int
    data: List[T]
