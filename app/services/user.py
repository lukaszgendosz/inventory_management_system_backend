from typing import List

from app.configs.exception.exception import NotFoundError, AlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemes.user import UserCreateScheme, UserUpdateScheme
from app.utils.security import hash_password



class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> List[User]:
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self._repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user
    
    def get_user_by_email(self, user_email: str) -> User:
        user = self._repository.get_by_email(user_email)
        return user

    def create_user(self, request: UserCreateScheme) -> User:
        user = self.get_user_by_email(request.email)
        if user:
            raise AlreadyExistsError('User already exists.')
        user = User(**request.model_dump())
        user.password = hash_password(request.password)
        user = self._repository.save(user)
        return user
    
    def update_user(self, user_id: int, request: UserUpdateScheme):
        user = self.get_user_by_id(user_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        return self._repository.save(user)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
