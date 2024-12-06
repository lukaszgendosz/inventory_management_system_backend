from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from app.configs.containers import Application
from app.services.auth import AuthService
from app.schemes import UserLoginScheme, TokenResponseScheme
from app.utils.dependencies import RefreshTokenBearer


router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


@router.post("/login")
@inject
async def login(
    request: UserLoginScheme,
    auth_service: AuthService = Depends(Provide[Application.services.auth_service]),
) -> TokenResponseScheme:
    return auth_service.login(request)


@router.post("/refresh")
@inject
async def refresh_token(
    token_details=Depends(RefreshTokenBearer()),
    auth_service: AuthService = Depends(Provide[Application.services.auth_service]),
) -> None:
    return auth_service.refresh_token(token_details)
