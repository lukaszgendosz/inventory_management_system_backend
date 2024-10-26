from typing import List

from app.configs.exception.exception import NotFoundError, AlreadyExistsError, AccessDeniedError
from app.repositories import UserRepository
from app.models import User
from app.schemes import UserCreateScheme, UserUpdateScheme, GenericFilterParams
from app.utils.security import hash_password


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self, params: GenericFilterParams) -> list[User]:
        return self._repository.get_paginated_list(params)

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
            raise AlreadyExistsError("User already exists.")
        user = User(**request.model_dump())
        user.password = hash_password(request.password)
        user = self._repository.save(user)
        return user

    def update_user(self, user_id: int, request: UserUpdateScheme) -> User:
        user = self.get_user_by_id(user_id)

        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        return self._repository.save(user)

    def deactivate_user(self, user_id: int, current_user: User) -> None:
        user = self.get_user_by_id(user_id)

        if user.id == current_user.id:
            raise AccessDeniedError("You cannot deactivate yourself.")

        user.is_active = False
        return self._repository.save(user)
