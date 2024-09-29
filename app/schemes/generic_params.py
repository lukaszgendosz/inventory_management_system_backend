from pydantic import BaseModel, Field

class GenericFilterParams(BaseModel):
    page_size: int = Field(25, gt=0, le=500)
    page: int = Field(1, gt=0)