from pydantic import BaseModel

class ApiErrorSchema(BaseModel):
    timestamp: int
    date: str
    msg: str