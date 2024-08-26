from app.configs.exception.exception import NotFoundError

from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemes.user import UserCreateScheme, UserUpdateScheme
from typing import List


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

    def create_user(self, request: UserCreateScheme) -> User:
        user = User(**request.model_dump())
        dupa = self._repository.save(user)
        return dupa
    
    def update_user(self, user_id: int, request: UserUpdateScheme):
        user = self.get_user_by_id(user_id)
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        return self._repository.save(user)

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)
