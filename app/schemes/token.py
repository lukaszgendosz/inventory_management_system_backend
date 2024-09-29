from pydantic import BaseModel


class TokenResponseScheme(BaseModel):
    access_token: str
    refresh_token: str
