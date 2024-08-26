from fastapi import APIRouter, Depends, status, HTTPException
from dependency_injector.wiring import inject, Provide
from collections.abc import Iterable

from app.services.user import UserService
from app.schemes.user import UserCreateScheme, UserResponseScheme, UserUpdateScheme
from app.configs.containers import Application

router = APIRouter(
    prefix='/api/v1'
)

@router.get('/users')
@inject
def get_users(
    user_service: UserService = Depends(Provide[Application.services.user_service])
    ) -> list[UserResponseScheme]:
    print(user_service)
    return user_service.get_users()

@router.get('/users/{user_id}')
@inject
def get_users(
    user_id: int,
    user_service: UserService = Depends(Provide[Application.services.user_service])
    ) -> UserResponseScheme:
    return user_service.get_user_by_id(user_id)


@router.post('/users')
@inject
def create_user(
    request: UserCreateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service])
    ) -> UserResponseScheme:
    return user_service.create_user(request)

@router.patch('/users/{user_id}')
@inject
def update_user(
    user_id: int,
    request: UserUpdateScheme,
    user_service: UserService = Depends(Provide[Application.services.user_service])
    ) -> UserResponseScheme:
    return user_service.update_user(user_id,request)