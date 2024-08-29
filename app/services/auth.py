from datetime import timedelta

from app.configs.exception.exception import AuthenticationError
from app.schemes import UserLoginScheme, TokenResponseScheme
from app.utils.security import verify_password, create_token
from .user import UserService




class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service
        
    def login(self, request: UserLoginScheme) -> None:
        user = self.user_service.get_user_by_email(request.email)
        if not user or not verify_password(request.password, user.password):
            raise AuthenticationError("Invalid email or password.")
        if not user.activated:
            raise AuthenticationError("Your account is not active. Contact your administrator.")
        data = {
            'user': {
                'id': user.id
            }
        }
        access_token = create_token(data)
        refresh_token = create_token(data,expires_delta=timedelta(days=1),is_refresh=True)
        return TokenResponseScheme(access_token=access_token, refresh_token=refresh_token)
        
        
        
        
        
        
        
        
        