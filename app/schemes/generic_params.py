from enum import Enum

from pydantic import BaseModel, Field


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class GenericFilterParams(BaseModel):
    page_size: int = Field(25, gt=0, le=500)
    page: int = Field(1, gt=0)
    search: str = Field("")
    order_by: str = Field("id")
    sort_order: SortOrder = Field(SortOrder.ASC)
