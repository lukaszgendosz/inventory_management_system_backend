from datetime import timedelta

from app.configs.exception.exception import AuthenticationError
from app.schemes import UserLoginScheme, TokenResponseScheme
from app.utils.security import verify_password, create_token
from .user import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def login(self, credentials: UserLoginScheme) -> TokenResponseScheme:
        user = self.user_service.get_user_by_email(credentials.email)

        if not user or not verify_password(credentials.password, user.password):
            raise AuthenticationError("Incorrect email address or password.")

        if not user.is_active:
            raise AuthenticationError(
                "Your account is not active. Please contact your administrator."
            )

        token_data = {"user": {"id": user.id}}

        access_token = create_token(token_data)
        refresh_token = create_token(token_data, expires_delta=timedelta(days=14), is_refresh=True)

        return TokenResponseScheme(
            access_token=access_token, refresh_token=refresh_token, role=user.role
        )

    def refresh_token(self, token_data: dict) -> None:
        user = self.user_service.get_user_by_id(token_data["user"]["id"])
        role = user.role
        new_access_token = create_token({"user": token_data["user"]})

        return TokenResponseScheme(access_token=new_access_token, refresh_token="", role=role)
