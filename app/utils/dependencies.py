from datetime import datetime

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, Depends
from dependency_injector.wiring import inject, Provide


from app.configs.exception.exception import AuthenticationError, AccessTokenRequired, RefreshTokenRequired
from app.configs.containers import Application
from app.schemes import Role
from app.models import User
from app.services import UserService
from .security import decode_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        self.verify_token_data(token_data)
        return token_data

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["is_refresh"]:
            raise AccessTokenRequired()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["is_refresh"]:
            raise RefreshTokenRequired()
 
@inject       
async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    user_service: UserService = Depends(Provide[Application.services.user_service]),
) -> User:
    user_id = token_details["user"]["id"]
    user = user_service.get_user_by_id(user_id)
    
    if not user.is_active:
        raise AuthenticationError(
                "Your account is not active. Please contact your administrator."
            )
    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if current_user.role in self.allowed_roles:
            return True

        raise AuthenticationError("You do not have permission to perform this action.")
    
user_role_checker = RoleChecker([Role.USER, Role.MANAGER, Role.ADMIN])
manager_role_checker = RoleChecker([Role.MANAGER, Role.ADMIN])
admin_role_checker = RoleChecker([Role.ADMIN])